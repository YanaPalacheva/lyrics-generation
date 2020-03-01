from gingerit.gingerit import GingerIt

import language_check

def ginger_errors(line, Typos = False):
    
    parser = GingerIt()
    parse = parser.parse(line)
    errors = parse['corrections']
    
    nontypos = [d for d in errors if d['definition'] != None]
    
    if Typos:
        return len(errors)
    else:
        return len(nontypos)
    
def mean_ginger_error(lyrics, Typos = False):
    total = 0
    # We have assumed lyrics is a list of strings corresponding to each line
    for line in lyrics:
        total += ginger_errors(line, Typos)
    return total/len(lyrics)

def ginger_file(filename, Typos = False):
    f = open(filename, "r")
    lyrics = f.readlines() 
    score = mean_ginger_error(lyrics, Typos)
    print(filename, "has mean grammatical error ", score)
    

def lang_errors(line, Typos = False):
    
    tool = language_check.LanguageTool('en-US')
    
    matches = tool.check(line)
    nontypos = [match for match in matches if match.category != 'Possible Typos']
    
    if Typos:
        return len(matches)
    else:
        return len(nontypos)
    
def mean_lang_error(lyrics, Typos = False):
    total = 0
    # We have assumed lyrics is a list of strings corresponding to each line
    for line in lyrics:
        total += lang_errors(line, Typos)
    return total/len(lyrics)

def lang_file(filename, Typos = False):
    f = open(filename, "r")
    lyrics = f.readlines() 
    score = mean_lang_error(lyrics, Typos)



def lang_typos(line):
    
    tool = language_check.LanguageTool('en-US')
    matches = tool.check(line)
    typos = [match for match in matches if match.category == 'Possible Typo' or match.category == 'Possible Typos']
    
    return len(typos)


# removal either by 'ginger' or by 'lang'
def nontypo_errors(line, remove = 'ginger'):
    if remove == 'ginger':
        return ginger_errors(line)
    if remove == 'lang':
        return ginger_errors(line, Typos = True) - lang_typos(line)
    print('Error: undefined removal')
    return None


def nontypo_mean(lyrics, remove = 'ginger'):
    total = 0
    for line in lyrics:
        total += nontypo_errors(line, remove)
    return total / len(lyrics)

def nontypo_file(filename, remove = 'ginger'):
    f = open(filename, "r")
    lyrics = f.readlines() 
    score = nontypo_mean(lyrics, remove)
    print(filename, "has mean grammatical error ", score)



