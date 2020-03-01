import re
import pronouncing
import nltk
import operator
import os
from multi_key_dict import multi_key_dict
from utils import split_file, get_last_word


def init_sound_dict():
    """
    Creates dictionary of similar morpheme groups.

    Morphemes are grouped by similarity, stressed (including secondary) are separated from unstressed,
    paired consonants are grouped together.

    :return: multi key dictionary with morpheme groups.
    """
    sound_dict = multi_key_dict()
    sound_dict['IY2', 'IY1', 'IH1', 'IH2', 'UH2', 'Y'] = ['IY2', 'IY1', 'IH1', 'IH2', 'UH2', 'Y']
    sound_dict['IH0', 'IY0'] = ['IH0', 'IY0']
    sound_dict['UW0', 'UH0'] = ['UW0', 'UH0']
    sound_dict['UW1', 'UW2', 'UH1'] = ['UW1', 'UW2', 'UH1']
    sound_dict['AA0', 'AH0'] = ['AA0', 'AH0']
    sound_dict['AA1', 'AA2', 'AH1', 'AH2'] = ['AA1', 'AA2', 'AH1', 'AH2']
    sound_dict['AY0'] = ['AY0']
    sound_dict['AY1', 'AY2'] = ['AY1', 'AY2']
    sound_dict['AW0'] = ['AW0']
    sound_dict['AW1', 'AW2'] = ['AW1', 'AW2']
    sound_dict['AO0'] = ['AO0']
    sound_dict['AO1', 'AO1', 'AO2'] = ['AO1', 'AO1', 'AO2']
    sound_dict['OY0'] = ['OY0']
    sound_dict['OY1', 'OY2'] = ['OY1', 'OY2']
    sound_dict['OW0'] = ['OW0']
    sound_dict['OW1', 'OW2'] = ['OW1', 'OW2']
    sound_dict['EY0'] = ['EY0']
    sound_dict['EY1', 'EY2'] = ['EY1', 'EY2']
    sound_dict['EH0', 'AE0'] = ['EH0', 'AE0']
    sound_dict['EH1', 'EH2', 'AE1', 'AE2'] = ['EH1', 'EH2', 'AE1', 'AE2']
    sound_dict['ER0'] = ['ER0']
    sound_dict['ER1', 'ER2'] = ['ER1', 'ER2']
    sound_dict['S', 'Z', 'DH', 'TH'] = ['S', 'Z', 'DH', 'TH']
    sound_dict['P', 'B'] = ['P', 'B']
    sound_dict['M', 'N', 'NG'] = ['M', 'N', 'NG']
    sound_dict['F', 'V'] = ['F', 'V']
    sound_dict['G', 'K'] = ['G', 'K']
    sound_dict['T', 'D'] = ['T', 'D']
    sound_dict['JH', 'CH'] = ['JH', 'CH']
    sound_dict['SH', 'ZH'] = ['SH', 'ZH']
    sound_dict['L'] = ['L']
    sound_dict['R'] = ['R']
    sound_dict['HH'] = ['HH']
    sound_dict['W'] = ['W']
    return sound_dict

class RhymerSyl:
    """
    Extended rhyme definition: based on 2-morpheme endings of words instead of 2-letter endings.
    """
    def __init__(self, identifier, generated=False):
        """
        Initializes Rhymer instance

        :param identifier: current artist or genre, str.
        :param generated: True for processing a machine generated text, else False.
        """
        self.rhyme_filename = f"rhymes/{identifier}.syl.rhymes"
        if generated:
            self.scheme_filename = f"schemes/{identifier}_generated.syl.schemes"
            self.lyrics_filename = f"generated_lyrics/{identifier}_syl_generated.txt"
        else:
            self.scheme_filename = f"schemes/{identifier}.syl.schemes"
            self.lyrics_filename = f"data/{identifier}.txt"
        self.entries = nltk.corpus.cmudict.entries()
        self.sound_dict = init_sound_dict()
        if os.path.exists(self.scheme_filename):
            with open(self.scheme_filename, "r", encoding='utf-8') as f:
                self.rhymeschemes = f.read().splitlines()

    def line_rhymescheme(self, line):
        """
        Creates rhyme scheme for a given line.

        :param line: line of lyrics, str
        :return: last two morphemes of the last word in line, str
        """
        end_word = re.sub(r"\W+", '', get_last_word(line)).lower()
        pronunciation_list = pronouncing.phones_for_word(end_word)
        if pronunciation_list:
            potential_rhymes = {}
            sound_pairs = []
            for item in pronunciation_list:
                sound_pair = item.split(' ')[-2:]
                if len(sound_pair) < 2:
                    for sound1 in self.sound_dict[sound_pair[0]]:
                        sound_pairs.append((sound1, ''))
                else:
                    for sound1 in self.sound_dict[sound_pair[0]]:
                        for sound2 in self.sound_dict[sound_pair[1]]:
                            sound_pairs.append((sound1, sound2))
            for sound_pair in sound_pairs:
                if sound_pair not in potential_rhymes.keys():
                    potential_rhymes[sound_pair] = 0
                if sound_pair[1] == '':
                    potential_rhymes[sound_pair] += len(pronouncing.search(sound_pair[0] + "$"))
                else:
                    potential_rhymes[sound_pair] += len(pronouncing.search(sound_pair[0] + " " + sound_pair[1] + "$"))
            most_freq_pair = max(potential_rhymes.items(), key=operator.itemgetter(1))[0]
            rhymescheme = most_freq_pair[0] + ' ' + most_freq_pair[1]
        else:
            rhymescheme = end_word[-2:]
        return rhymescheme

    def create_rhymescheme(self):
        """
        Creates rhyme scheme list for lyrics and writes it to a file
        """
        lyrics = split_file(self.lyrics_filename)
        schemes = []
        for i, line in enumerate(lyrics):
            schemes.append(self.line_rhymescheme(line))
        with open(self.scheme_filename, "w", encoding='utf-8') as f:
            f.write('\n'.join(schemes) + '\n')

    def rhymeindex(self, lyrics):
        """
        Creates a list of the most frequent rhyming word endings in lyrics.

        :param lyrics: list of lines in lyrics, str[]
        :return: list of sorted 2-morpheme rhyme ends, str[]
        """
        rhyme_master_list = []
        print("Building list of rhymes:")
        for i, line in enumerate(lyrics):
            rhymescheme = self.rhymeschemes[i]
            rhyme_master_list.append(rhymescheme)
        rhyme_master_list = list(set(rhyme_master_list))
        reverselist = [x[::-1] for x in rhyme_master_list]
        reverselist = sorted(reverselist)
        rhymelist = [x[::-1] for x in reverselist]

        print("List of Sorted 2-Morpheme Rhyme Ends:")
        print(rhymelist)
        with open(self.rhyme_filename, "w", encoding='utf-8') as f:
            f.write("\n".join(rhymelist))
        return rhymelist

    def rhyme(self, i, line, rhyme_list, generated=False):
        """
        Counts rhyme frequency score from sorted morpheme endings.

        :param i: line number, int
        :param line: line of lyrics, str
        :param rhyme_list: list of 2-morpheme rhyme endings, str[]
        :param generated: True if line was generated by markovify function, False for actual lyrics.
        :return: rhyme frequency score, float
        """
        if generated:
            float_rhyme = rhyme_list.index(self.line_rhymescheme(line))
        else:
            float_rhyme = rhyme_list.index(self.rhymeschemes[i])
        if rhyme_list:
            float_rhyme = float_rhyme / float(len(rhyme_list))
            return float_rhyme
        else:
            return 0
