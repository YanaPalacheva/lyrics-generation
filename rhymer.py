import re
import pronouncing
import nltk
import operator
import os
from multi_key_dict import multi_key_dict
from utils import split_file


def init_sound_dict():
    sound_dict = multi_key_dict()
    sound_dict['IH0', 'IY2', 'IY1', 'IY0', 'IH1', 'IH2', 'UH2', 'Y', 'i'] = ['IH0', 'IY2', 'IY1', 'IY0', 'IH1', 'IH2',
                                                                             'UH2', 'Y']
    sound_dict['UW0', 'UW1', 'UW2', 'UH0', 'UH1', 'u'] = ['UW0', 'UW1', 'UW2', 'UH0', 'UH1']
    sound_dict['AA1', 'AA0', 'AA2', 'AH0', 'AH1', 'AH2', 'a'] = ['AA1', 'AA0', 'AA2', 'AH0', 'AH1', 'AH2']
    sound_dict['AY1', 'AY2', 'AY0', 'ay'] = ['AY1', 'AY2', 'AY0']
    sound_dict['AW0', 'AW1', 'AW2', 'aw'] = ['AW0', 'AW1', 'AW2']
    sound_dict['AO1', 'AO1', 'AO2', 'o'] = ['AO1', 'AO1', 'AO2']
    sound_dict['OY0', 'OY1', 'OY2', 'oy'] = ['OY0', 'OY1', 'OY2']
    sound_dict['OW0', 'OW1', 'OW2', 'ow'] = ['OW0', 'OW1', 'OW2']
    sound_dict['EY0', 'EY1', 'EY2', 'ey'] = ['EY0', 'EY1', 'EY2']
    sound_dict['EH0', 'EH1', 'EH2', 'AE1', 'AE0', 'AE2', 'e'] = ['EH0', 'EH1', 'EH2', 'AE1', 'AE0', 'AE2']
    sound_dict['ER1', 'ER0', 'ER2', 'er'] = ['ER1', 'ER0', 'ER2']
    sound_dict['S', 'Z', 'DH', 'TH', 's', 'z', 'th'] = ['S', 'Z', 'DH', 'TH']
    sound_dict['P', 'B', 'p', 'b'] = ['P', 'B']
    sound_dict['M', 'N', 'NG', 'm', 'n', 'ng'] = ['M', 'N', 'NG']
    sound_dict['F', 'V', 'f', 'v'] = ['F', 'V']
    sound_dict['G', 'K', 'g', 'k'] = ['G', 'K']
    sound_dict['T', 'D', 't', 'd'] = ['T', 'D']
    sound_dict['JH', 'CH', 'ge', 'ch'] = ['JH', 'CH']
    sound_dict['SH', 'ZH', 'sh', 'zh'] = ['SH', 'ZH']
    sound_dict['L', 'l'] = ['L']
    sound_dict['R', 'r'] = ['R']
    sound_dict['HH'] = ['HH']
    sound_dict['W'] = ['W']
    return sound_dict


class Rhymer:
    def __init__(self, identifier):
        self.rhyme_filename = f"rhymes/{identifier}.rhymes"
        self.scheme_filename = f"schemes/{identifier}.schemes"
        self.lyrics_filename = f"data/{identifier}.txt"
        self.entries = nltk.corpus.cmudict.entries()
        self.sound_dict = init_sound_dict()
        if os.path.exists(self.scheme_filename):
            with open(self.scheme_filename, "r", encoding='utf-8') as f:
                self.rhymeschemes = f.read().splitlines()

    def line_rhymescheme(self, line):
        end_word = re.sub(r"\W+", '', line.split(" ")[-1]).lower()
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
        lyrics = split_file(self.lyrics_filename)
        schemes = []
        for i, line in enumerate(lyrics):
            schemes.append(self.line_rhymescheme(line))
        with open(self.scheme_filename, "w", encoding='utf-8') as f:
            f.write('\n'.join(schemes) + '\n')

    def rhymeindex(self, lyrics):
        rhyme_master_list = []
        print("Building list of rhymes:")
        for i, line in enumerate(lyrics):
            rhymescheme = self.rhymeschemes[i]
            rhyme_master_list.append(rhymescheme)
        rhyme_master_list = list(set(rhyme_master_list))
        reverselist = [x[::-1] for x in rhyme_master_list]
        reverselist = sorted(reverselist)
        rhymelist = [x[::-1] for x in reverselist]

        print("List of Sorted 2-Letter Rhyme Ends:")
        print(rhymelist)
        with open(self.rhyme_filename, "w", encoding='utf-8') as f:
            f.write("\n".join(rhymelist))
        return rhymelist

    def rhyme(self, i, line, rhyme_list, generated=False):
        if generated:
            float_rhyme = rhyme_list.index(self.line_rhymescheme(line))
        else:
            float_rhyme = rhyme_list.index(self.rhymeschemes[i])
        if rhyme_list:
            float_rhyme = float_rhyme / float(len(rhyme_list))
            return float_rhyme
        else:
            return 0