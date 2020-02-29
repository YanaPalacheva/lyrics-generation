import numpy as np
import random
import pronouncing
import re
import os
from nn_model import LyricsNN
from utils import create_markov_model, split_file


class LyricsGenerator:
    def __init__(self, max_syllables, identifier, nn_depth):
        self.max_syllables = max_syllables
        self.identifier = identifier
        self.rhyme_filename = f"rhymes/{self.identifier}.rhymes"
        self.training_file = f"data/{identifier}.txt"
        self.lyrics_model = LyricsNN(nn_depth, identifier)
        self.markov_model = create_markov_model(self.training_file)
        self.original_bars = split_file(self.training_file)

    def training_phase(self):
        rhyme_list = self.rhymeindex(self.original_bars)
        x_data, y_data = self.build_dataset(self.original_bars, rhyme_list)
        self.lyrics_model.train(x_data, y_data)

    def generating_phase(self):
        markov_bars = self.generate_lyrics()
        if os.path.exists(self.rhyme_filename):
            rhyme_list = split_file(self.rhyme_filename)
        else:
            rhyme_list = self.rhymeindex(markov_bars)
        vectors = self.create_vectors(rhyme_list)
        lyrics = self.vectors_into_lyrics(vectors, markov_bars, rhyme_list)
        f = open(f"generated_lyrics/{self.identifier}_generated.txt", "w", encoding='utf-8')
        for bar in lyrics:
            f.write(bar)
            f.write("\n")

    def build_dataset(self, lines, rhyme_list):
        dataset = []
        for line in lines:
            line_list = [self.syllables(line), self.rhyme(line, rhyme_list)]
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
        # count = 0

        while len(bars) < len(self.original_bars) / 4:
            bar = self.markov_model.make_sentence(max_overlap_ratio=0.49, tries=50)
            if bar and self.syllables(bar) < 1:
                last_word = bar.split(" ")[-1]
                if bar not in bars and last_words.count(last_word) < 3:
                    bars.append(bar)
                    last_words.append(last_word)
        return bars

    def create_vectors(self, rhyme_list):
        lyrics_vectors = []
        initial_index = random.choice(range(len(self.original_bars) - 1))
        initial_lines = self.original_bars[initial_index:initial_index + 2]
        starting_input = []
        for line in initial_lines:
            starting_input.append([self.syllables(line), self.rhyme(line, rhyme_list)])
        starting_vectors = self.lyrics_model.predict(np.array([starting_input]).flatten().reshape(1, 2, 2))
        lyrics_vectors.append(starting_vectors)
        for i in range(20):  # number of 2-lines to be generated
            lyrics_vectors.append(self.lyrics_model.predict(np.array([lyrics_vectors[-1]]).flatten().reshape(1, 2, 2)))
        return lyrics_vectors

    def vectors_into_lyrics(self, vectors, markov_bars, rhyme_list):
        print("Writing verse:\n")

        def last_word_compare(lyrics, line2):
            penalty = 0
            for line1 in lyrics:
                word1 = line1.split(" ")[-1]
                word2 = line2.split(" ")[-1]
                if len(word1) > 1 and len(word2) > 1 and word1 == word2:
                    penalty += 0.2
            return penalty

        def calculate_score(vector_half, syllables, rhyme, penalty):
            desired_syllables = vector_half[0]
            desired_rhyme = vector_half[1]
            desired_syllables = desired_syllables * self.max_syllables
            desired_rhyme = desired_rhyme * len(rhyme_list)
            score = 1.0 - abs(float(desired_syllables) - float(syllables)) + abs(
                float(desired_rhyme) - float(rhyme)) - penalty
            return score

        dataset = []
        print(len(markov_bars))
        for line in markov_bars:
            line_list = [line, self.syllables(line), self.rhyme(line, rhyme_list)]
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
        count = 0
        for word in line.split(" "):
            vowels = 'aeiouy'
            word = word.lower().strip(".:;?!")
            if word:
                if word[0] in vowels:
                    count += 1
                for index in range(1, len(word)):
                    if word[index] in vowels and word[index - 1] not in vowels:
                        count += 1
                if word.endswith('e'):
                    count -= 1
                if word.endswith('le'):
                    count += 1
                if count == 0:
                    count += 1
        return count / self.max_syllables

    def rhymeindex(self, lyrics):
        rhyme_master_list = []
        print("Building list of rhymes:")
        for i in lyrics:
            word = re.sub(r"\W+", '', i.split(" ")[-1]).lower()
            rhymeslist = pronouncing.rhymes(word)
            rhymeslistends = []
            for i in rhymeslist:
                rhymeslistends.append(i[-2:])
            try:
                rhymescheme = max(set(rhymeslistends), key=rhymeslistends.count)
            except Exception:
                rhymescheme = word[-2:]
            rhyme_master_list.append(rhymescheme)
        rhyme_master_list = list(set(rhyme_master_list))
        reverselist = [x[::-1] for x in rhyme_master_list]
        reverselist = sorted(reverselist)
        rhymelist = [x[::-1] for x in reverselist]

        print("List of Sorted 2-Letter Rhyme Ends:")
        print(rhymelist)
        f = open(self.rhyme_filename, "w", encoding='utf-8')
        f.write("\n".join(rhymelist))
        f.close()
        return rhymelist

    def rhyme(self, line, rhyme_list):
        word = re.sub(r"\W+", '', line.split(" ")[-1]).lower()
        rhymeslist = pronouncing.rhymes(word)
        rhymeslistends = []
        for i in rhymeslist:
            rhymeslistends.append(i[-2:])
        try:
            rhymescheme = max(set(rhymeslistends), key=rhymeslistends.count)
        except Exception:
            rhymescheme = word[-2:]
        try:
            float_rhyme = rhyme_list.index(rhymescheme)
            float_rhyme = float_rhyme / float(len(rhyme_list))
            return float_rhyme
        except Exception:
            float_rhyme = 0
            return float_rhyme