import numpy as np
import random
import os
import pronouncing
from nn_model import LyricsNN
from utils import create_markov_model, split_file, count_syllables, get_last_word
from rhymer import Rhymer
from rhymer_old import RhymerOld


class LyricsGenerator:
    def __init__(self, identifier, params, old=False):
        self.params = params
        self.identifier = identifier
        if old:
            self.rhymer = RhymerOld(identifier)
        else:
            self.rhymer = Rhymer(identifier)
        self.training_file = f"data/{identifier}.txt"
        self.lyrics_model = LyricsNN(self.params['depth'], identifier)
        self.markov_model = create_markov_model(self.training_file)
        self.original_bars = split_file(self.training_file)

    def training_phase(self):
        rhyme_list = self.rhymer.rhymeindex(self.original_bars)
        x_data, y_data = self.build_dataset(self.original_bars, rhyme_list)
        self.lyrics_model.train(x_data, y_data)

    def generating_phase(self):
        markov_bars = self.generate_lyrics()
        if os.path.exists(self.rhymer.rhyme_filename):
            rhyme_list = split_file(self.rhymer.rhyme_filename)
        else:
            print("Rhyme list was not created, please train the model first.")
        vectors = self.create_vectors(rhyme_list)
        lyrics = self.vectors_into_lyrics(vectors, markov_bars, rhyme_list)
        f = open(f"generated_lyrics/{self.identifier}_generated.txt", "w", encoding='utf-8')
        for bar in lyrics:
            f.write(bar)
            f.write("\n")

    def build_dataset(self, lines, rhyme_list):
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
        bars = []
        last_words = []
        overlap = self.params['max_overlap']
        while len(bars) < self.params['gen_lyrics_len']:
            bar = self.markov_model.make_sentence(max_overlap_ratio=overlap, tries=50)
            if bar and self.syllables(bar) < 1:
                last_word = get_last_word(bar)
                if bar not in bars and last_words.count(last_word) < 3:
                    bars.append(bar)
                    last_words.append(last_word)
        return bars

    def create_vectors(self, rhyme_list):
        lyrics_vectors = []
        initial_index = random.choice(range(len(self.original_bars) - 1))
        initial_lines = self.original_bars[initial_index:initial_index + 2]
        starting_input = []
        for i, line in enumerate(initial_lines):
            starting_input.append([self.syllables(line), self.rhymer.rhyme(i, line, rhyme_list)])
        starting_vectors = self.lyrics_model.predict(np.array([starting_input]).flatten().reshape(1, 2, 2))
        lyrics_vectors.append(starting_vectors)
        for i in range(self.params['gen_lyrics_len']):  # number of 2-lines to be generated
            lyrics_vectors.append(self.lyrics_model.predict(np.array([lyrics_vectors[-1]]).flatten().reshape(1, 2, 2)))
        return lyrics_vectors

    def vectors_into_lyrics(self, vectors, markov_bars, rhyme_list):
        print("Writing verse:\n")

        def last_word_compare(lyrics, line2):
            penalty = 0
            for line1 in lyrics:
                word1 = get_last_word(line1)
                word2 = get_last_word(line2)
                if len(word1) > 1 and len(word2) > 1 and word1 == word2:
                    penalty += 0.2
            return penalty

        def calculate_score(vector_half, syllables, rhyme, penalty):
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
                    print(str(item[0]))
                    for i in dataset:
                        if item[0] == i[0]:
                            dataset.remove(i)
                            break
                    break
        return lyrics

    def syllables(self, line):
        count = count_syllables(line)
        return count / self.params['max_syllables']
