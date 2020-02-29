import language_check
import grammarbot
from grammarbot import GrammarBotClient

def lang_errors(line):
    
    tool = language_check.LanguageTool('en-US')
    
    matches = tool.check(line)
    return len(matches)

def bot_errors(line):
    
    client = GrammarBotClient()
    res = client.check(line)
    return len(res.matches)


# Assumes line is in the form of a string, tool either 'language_check' or 'grammarbot'

def num_errors(line, tool = 'language_check'):
    if tool == 'language_check':
        return lang_errors(line)
    if tool == 'grammarbot':
        return bot_errors(line)

def mean_grammatical_error(lyrics, tool = 'language_check'):
    total = 0
    # We have assumed lyrics is a list of strings corresponding to each line
    for line in lyrics:
        total += num_errors()
    return total/len(lyrics)