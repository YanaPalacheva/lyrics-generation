import markovify
import pronouncing


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
