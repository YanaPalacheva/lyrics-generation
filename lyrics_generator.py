import numpy as np
import random
import os
from nn_model import LyricsNN
from utils import create_markov_model, split_file, count_syllables, get_last_word
from rhymer_end import RhymerEnd
from rhymer_syl import RhymerSyl


class LyricsGenerator:
    def __init__(self, identifier, params, syllable_rhyme=False):
        """
        Initialization of LyricsGenerator class providing methods for generation of lyrics based on Markov chains and
        RNN: it generates markov sequences based on word1->word2 transition probabilities (markovify library) and
        uses an LSTM network to pick the most suitable sequence (LyricsNN class).
        :param identifier: current artist or genre, str
        :param params: contains depth, max_syllables, max_overlap, num_lines parameters, dict
        :param syllable_rhyme: True if we use morpheme based rhyme, False if we use 2-last-letters based rhyme, bool
        """
        self.params = params
        self.identifier = identifier
        if syllable_rhyme:
            self.rhymer = RhymerSyl(identifier)
            self.path_modifier = '_syl'
        else:
            self.rhymer = RhymerEnd(identifier)
            self.path_modifier = ''
        self.training_file = f"data/{identifier}.txt"
        self.lyrics_model = LyricsNN(self.params['depth'], identifier)
        self.markov_model = create_markov_model(self.training_file)
        self.original_bars = split_file(self.training_file)

    def training_phase(self):
        """
        Training phase: creation of list of two 2-morpheme or 2-letter endings (based on training data)
        and training of an LSTM network (self.lyrics_model, instance of LyricsNN class)
        """
        rhyme_list = self.rhymer.rhymeindex(self.original_bars)
        x_data, y_data = self.build_dataset(self.original_bars, rhyme_list)
        self.lyrics_model.train(x_data, y_data)

    def generating_phase(self):
        """
        Generation phase: consecutive creation and filtering of markov sequences and vectors and
        converting these vectors into lyrics.
        :return: generated lyrics, str
        """
        markov_bars = self.generate_lyrics()
        if os.path.exists(self.rhymer.rhyme_filename):
            rhyme_list = split_file(self.rhymer.rhyme_filename)
        else:
            print("Rhyme list was not created, please train the model first.")
            return
        vectors = self.create_vectors(rhyme_list)
        lyrics = self.vectors_into_lyrics(vectors, markov_bars, rhyme_list)
        f = open(f"generated_lyrics/{self.identifier}{self.path_modifier}_generated.txt", "w", encoding='utf-8')
        lyrics_str = ''
        for bar in lyrics:
            f.write(bar)
            f.write("\n")
            lyrics_str += bar + '\n'
        return lyrics_str

    def build_dataset(self, lines, rhyme_list):
        """
        Building datasets for LSTM training: one contains syllable and rhyme scores for odd couplets (two lines),
        another - the same information about even couplets.
        :param lines: training lyrics lines, list
        :param rhyme_list: list two 2-morpheme or 2-letter endings (based on training data), list
        :return datasets containing information about odd and even couplets (syllables and rhyme vectors), np array
        """
        dataset = []
        for i, line in enumerate(lines):
            line_list = [self.syllables(line), self.rhymer.rhyme(i, line, rhyme_list)]
            dataset.append(line_list)
        x_data = []
        y_data = []
        for i in range(len(dataset) - 3):
            line1 = dataset[i]
            line2 = dataset[i + 1]
            line3 = dataset[i + 2]
            line4 = dataset[i + 3]
            x = np.array([line1[0], line1[1], line2[0], line2[1]]).reshape(2, 2)
            x_data.append(x)
            y = np.array([line3[0], line3[1], line4[0], line4[1]]).reshape(2, 2)
            y_data.append(y)
        x_data = np.array(x_data)
        y_data = np.array(y_data)
        return x_data, y_data

    def generate_lyrics(self):
        """
        Generate a list of markov sequences (of size 5 * desired output size)
        and filter out lines with repetitive last word (not more than 2 lines with similar last word are permitted)
        :return: filtered markov sequences, list
        """
        bars = []
        last_words = []
        overlap = self.params['max_overlap']
        while len(bars) < self.params['num_lines'] * 5:
            bar = self.markov_model.make_sentence(max_overlap_ratio=overlap, tries=50)
            if bar and self.syllables(bar) < 1:
                last_word = get_last_word(bar)
                if bar not in bars and last_words.count(last_word) < 3:
                    bars.append(bar)
                    last_words.append(last_word)
        return bars

    def create_vectors(self, rhyme_list):
        """
        Generation of vectors with trained LSTM network based on initial lines and rhyme list.
        :param rhyme_list: list of two 2-morpheme or 2-letter endings (based on training data), list
        :return: list of vectors predicted by LSTM network
        """
        lyrics_vectors = []
        initial_index = random.choice(range(len(self.original_bars) - 1))
        initial_lines = self.original_bars[initial_index:initial_index + 2]
        starting_input = []
        for i, line in enumerate(initial_lines):
            starting_input.append([self.syllables(line), self.rhymer.rhyme(i, line, rhyme_list)])
        starting_vectors = self.lyrics_model.predict(np.array([starting_input]).flatten().reshape(1, 2, 2))
        lyrics_vectors.append(starting_vectors)
        for i in range(self.params['num_lines']):  # number of 2-lines to be generated
            lyrics_vectors.append(self.lyrics_model.predict(np.array([lyrics_vectors[-1]]).flatten().reshape(1, 2, 2)))
        return lyrics_vectors

    def vectors_into_lyrics(self, vectors, markov_bars, rhyme_list):
        """
        Producing a list of the generated lines based on vectors with the highest scores.
        :param vectors: vectors predicted by LSTM network, list
        :param markov_bars: list of filtered markov sequences, list
        :param rhyme_list: list of two 2-morpheme or 2-letter endings, list
        :return: generated lyrics lines, list
        """
        print("Writing lyrics:\n")

        def last_word_compare(lyrics, line2):
            """
            Calculation of penalty score for lines within generated lyrics having the similar to line2 last word.
            :param lyrics: list of generated lines, list
            :param line2: generated line to compare
            :return: penalty score, float
            """
            penalty = 0
            for line1 in lyrics:
                word1 = get_last_word(line1)
                word2 = get_last_word(line2)
                if len(word1) > 1 and len(word2) > 1 and word1 == word2:
                    penalty += 0.2
            return penalty

        def calculate_score(vector_half, syllables, rhyme, penalty):
            """
            Calculation of a final score for the generated line.
            :param vector_half: vector containing syllable and rhyme score for a line, np array
            :param syllables: syllable score of the generated line, float
            :param rhyme: rhyme score of the generated line, float
            :param penalty: penalty score for repetitive last words within lyrics, float
            :return: final score, float
            """
            desired_syllables = vector_half[0]
            desired_rhyme = vector_half[1]
            desired_syllables = desired_syllables * self.params['max_syllables']
            desired_rhyme = desired_rhyme * len(rhyme_list)
            score = 1.0 - abs(float(desired_syllables) - float(syllables)) + abs(
                float(desired_rhyme) - float(rhyme)) - penalty
            return score

        dataset = []
        for line in markov_bars:
            line_list = [line, self.syllables(line), self.rhymer.rhyme(0, line, rhyme_list, generated=True)]
            dataset.append(line_list)
        lyrics = []
        vector_halves = []
        for vector in vectors:
            vector_halves.append(list(vector[0][0]))
            vector_halves.append(list(vector[0][1]))
        for vector in vector_halves:
            scorelist = []
            for item in dataset:
                line = item[0]
                if len(lyrics) != 0:
                    penalty = last_word_compare(lyrics, line)
                else:
                    penalty = 0
                total_score = calculate_score(vector, item[1], item[2], penalty)
                score_entry = [line, total_score]
                scorelist.append(score_entry)
            fixed_score_list = [0]
            for score in scorelist:
                fixed_score_list.append(float(score[1]))
            max_score = max(fixed_score_list)
            for item in scorelist:
                if item[1] == max_score:
                    lyrics.append(item[0])
                    print(str(item[0]))  # writing generated lyrics into console
                    for i in dataset:
                        if item[0] == i[0]:
                            dataset.remove(i)
                            break
                    break
        return lyrics

    def syllables(self, line):
        """
        Calculation of a syllable score for a line: num of syllables in the line / max_syllables param
        :param line: target line, str
        :return: syllable score, float
        """
        count = count_syllables(line)
        return count / self.params['max_syllables']
