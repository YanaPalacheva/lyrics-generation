import language_check
from grammarbot import GrammarBotClient


def lang_errors(line):
    tool = language_check.LanguageTool('en-US')
    matches = tool.check(line)
    return len(matches)


def bot_errors(line):
    client = GrammarBotClient()
    res = client.check(line)
    print(line)
    print(res.matches)
    print('-------')
    return len(res.matches)


# Assumes line is in the form of a string, tool either 'language_check' or 'grammarbot'
def num_errors(line, tool):
    if tool == 'language_check':
        return lang_errors(line)
    if tool == 'grammarbot':
        return bot_errors(line)


def mean_grammatical_error(lyrics, tool='language_check'):
    total = 0
    # We have assumed lyrics is a list of strings corresponding to each line
    for line in lyrics:
        total += num_errors(line, tool)
    return total/len(lyrics)

from utils import split_file
print(bot_errors('I ate it up and spit it out'))
# original_bars = split_file(f'data/frank-sinatra.txt')
# print(mean_grammatical_error(original_bars[:50], 'grammarbot'))
