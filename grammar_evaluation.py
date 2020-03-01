from gingerit.gingerit import GingerIt

import language_check

def ginger_errors(line, Typos = False):
    """Computes number of grammatical errors in a line of lyrics based on Gingerit parser

Args:
    line (str): a line of lyrics represented as a string value
    Typos (bool): a boolean value specifying whether to include typos

Returns:
    number of errors (int)
"""
    parser = GingerIt()
    parse = parser.parse(line)
    errors = parse['corrections']
    
    nontypos = [d for d in errors if d['definition'] != None]
    
    if Typos:
        return len(errors)
    else:
        return len(nontypos)
    
def mean_ginger_error(lyrics, Typos = False):
    """Computes average number of grammatical errors in an entire lyrics based on Gingerit parser


Args:
    lyrics (str[]): a list of lyrics lines
    Typos (bool): a boolean value specifying whether to include typos

Returns:
    average number of errors per line (float)
"""
    total = 0
    # We have assumed lyrics is a list of strings corresponding to each line
    for line in lyrics:
        total += ginger_errors(line, Typos)
    return total/len(lyrics)

def ginger_file(filename, Typos = False):
"""Prints average number of grammatical errors per line of lyrics based on Gingerit parser


Args:
    filename (str): name of file containing lyrics
    Typos (bool): a boolean value specifying whether to include typos

Returns:
    None
"""

    f = open(filename, "r")
    lyrics = f.readlines() 
    score = mean_ginger_error(lyrics, Typos)
    print(filename, "has mean grammatical error ", score)
    

def lang_errors(line, Typos = False):
    """Computes number of grammatical errors in a line of lyrics based on language_check parser

Args:
    line (str): a line of lyrics represented as a string value
    Typos (bool): a boolean value specifying whether to include typos

Returns:
    number of errors (int)
"""
    tool = language_check.LanguageTool('en-US')
    
    matches = tool.check(line)
    nontypos = [match for match in matches if match.category != 'Possible Typos']
    
    if Typos:
        return len(matches)
    else:
        return len(nontypos)
    
def mean_lang_error(lyrics, Typos = False):
    """Computes average number of grammatical errors in an entire lyrics based on language_check parser


Args:
    lyrics (str[]): a list of lyrics lines
    Typos (bool): a boolean value specifying whether to include typos

Returns:
    average number of errors per line (float)
"""

    total = 0
    # We have assumed lyrics is a list of strings corresponding to each line
    for line in lyrics:
        total += lang_errors(line, Typos)
    return total/len(lyrics)

def lang_file(filename, Typos = False):
"""Prints average number of grammatical errors per line of lyrics based on language_check parser


Args:
    filename (str): name of file containing lyrics
    Typos (bool): a boolean value specifying whether to include typos

Returns:
    None
"""

    f = open(filename, "r")
    lyrics = f.readlines() 
    score = mean_lang_error(lyrics, Typos)



def lang_typos(line):
"""Computes number of typos in a line of lyrics based on language_check parser


Args:
    line (str): line of lyrics represented as string value


Returns:
    number of typos (int)
"""

    
    tool = language_check.LanguageTool('en-US')
    matches = tool.check(line)
    typos = [match for match in matches if match.category == 'Possible Typo' or match.category == 'Possible Typos']
    
    return len(typos)


# removal either by 'ginger' or by 'lang'
def nontypo_errors(line, remove = 'ginger'):
"""Computes number of non-typo errors in a line of lyrics by first counting all errors with Gingerit parser, then subtracting typos by either Gingerit of language_check parser


Args:
    line (str): line of lyrics represented as string value
    remove (str): name of parser used to remove typos; either 'ginger' or 'lang'


Returns:
    number of non-typo errors (int)
"""

    if remove == 'ginger':
        return ginger_errors(line)
    if remove == 'lang':
        return ginger_errors(line, Typos = True) - lang_typos(line)
    print('Error: undefined removal')
    return None


def nontypo_mean(lyrics, remove = 'ginger'):
"""Computes average number of non-typo errors per line in lyrics using the nontypo_errors method.


Args:
    lyrics (str[]): list of lyrics lines
    remove (str): name of parser used to remove typos; either 'ginger' or 'lang'


Returns:
    average number of non-typo errors (float)
"""

    total = 0
    for line in lyrics:
        total += nontypo_errors(line, remove)
    return total / len(lyrics)

def nontypo_file(filename, remove = 'ginger'):
"""Prints average number of grammatical errors per line of lyrics based on the nontypo_errors method.


Args:
    filename (str): name of file containing lyrics
    remove (str): name of parser used to remove typos; either 'ginger' or 'lang'

Returns:
    None
"""

    f = open(filename, "r")
    lyrics = f.readlines() 
    score = nontypo_mean(lyrics, remove)
    print(filename, "has mean grammatical error ", score)



