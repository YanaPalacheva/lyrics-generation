import language_check

def num_errors(line, Typos = False):
    
    tool = language_check.LanguageTool('en-US')
    
    matches = tool.check(line)
    nontypos = [match for match in matches if match.category != 'Possible Typos']
    if not Typos:
        return len(nontypos)
    else:
        return len(matches)

def mean_grammatical_error(lyrics, Typos = False):
    total = 0
    # We have assumed lyrics is a list of strings corresponding to each line
    for line in lyrics:
        total += num_errors(line, Typos)
    return total/len(lyrics)


def grammar_check_file(filename, Typos = False):
    f = open(filename, "r")
    lyrics = f.readlines() 
    score = mean_grammatical_error(lyrics, Typos)
    print(filename, "has mean grammatical error ", score)
    #print('hello world')
    
grammar_check_file("freddie-mercury.txt", True)
grammar_check_file("freddie-mercury_generated.txt", True)

