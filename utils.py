import markovify


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
