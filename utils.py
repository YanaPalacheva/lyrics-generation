import markovify
import pronouncing

default_params = {'num_lines': 40, 'depth': 4,
                  'syl_overlap': {'50-cent': (11, 0.5), 'elvis-presley': (9, 0.7),
                                  'freddie-mercury': (9, 0.7), 'evanescence': (8, 0.75),
                                  'enya': (7, 0.8), 'frank-sinatra': (9, 0.7), 'depeche-mode': (7, 0.8),
                                  'ed-sheeran': (9, 0.8), 'david-bowie': (8, 0.75),
                                  'hip-hop': (11, 0.5), 'folk-country': (9, 0.7), 'jazz': (9, 0.7),
                                  'rock': (9, 0.7), 'electronic': (7, 0.8), 'pop': (9, 0.7)}}


def create_markov_model(training_file):
    read = open(training_file, "r", encoding='utf-8').read()
    text_model = markovify.NewlineText(read)
    return text_model


def split_file(file):
    text = open(file, encoding='utf-8').read()
    text = text.split("\n")
    while "" in text:
        text.remove("")
    return text


def unknown_word_syllables(word):
    count = 0
    vowels = 'aeiouy'
    if word:
        if word[0] in vowels:
            count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
        if len(word) > 2 and word.endswith('e'):
            count -= 1
        if word.endswith('le'):
            count += 1
        if count == 0:
            count += 1
    return count


def count_syllables(line):
    count = 0
    for word in line.split(" "):
        word = word.lower()
        pronunciation_list = pronouncing.phones_for_word(word)
        if pronunciation_list:
            count += pronouncing.syllable_count(pronunciation_list[0])
        else:
            count += unknown_word_syllables(word)
    return count


def get_last_word(line):
    return line.split(" ")[-1]
