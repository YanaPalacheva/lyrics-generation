import random
from gingerit.gingerit import GingerIt
import language_check


def tool_errors(line,  allow_typos=False, parser=None):
    """
    Computes number of grammatical errors in a line of lyrics
        :param line: a line of lyrics represented as a string value, str
        :param allow_typos: a boolean value specifying whether to include typos, bool
        :param parser: parser instance, GingerIt; None for LanguageTool
        :return: number of errors, int
    """
    if parser:
        parse = parser.parse(line)
        errors = parse['corrections']
        nontypos = [err for err in errors if err['definition'] and not err['definition'].endswith(' not')]
    else:
        tool = language_check.LanguageTool('en-US')
        errors = tool.check(line)
        nontypos = [err for err in errors if err.category != 'Possible Typos']
    if allow_typos:
        return len(errors)
    else:
        return len(nontypos)
    
def long_errors(line,  allow_typos=False, parser=None):
    """
    Computes number of grammatical errors in a possibly longer line of lyrics
        :param line: a line of lyrics represented as a string value, str
        :param allow_typos: a boolean value specifying whether to include typos, bool
        :param parser: parser instance, GingerIt; None for LanguageTool
        :return: number of errors, int
    """
    l = len(line)
    if l < 400:
        return tool_errors(line, allow_typos, parser)
    else:
        n = 0
        i = 0
        while 100*i + 300 < l:
            n += tool_errors(line[100*i: 100*i + 400], allow_typos, parser)
            i += 1
        j = i - 1
        return (l / (400*j + (l-100*j))) * n


def mean_error(lyrics, allow_typos=False, parser=None, combined=False, filename = '', index = None):
    """
    Computes average number of grammatical errors in an entire lyrics based on Gingerit parser
    :param lyrics: a list of lyrics lines, str[]
    :param allow_typos: a boolean value specifying whether to include allow_typos, bool
    :param parser: parser instance, GingerIt; None for LanguageTool
    :param combined: a boolean value specifying whether to combine tools in case parser is GingerIt, bool
    :param filename: a string value specifying name of file lyrics came from if necessary for other applications
    :return: average number of errors per line, float
    """
    combined = parser and combined and not allow_typos # consider combined only in case parser is GingerIt and we don't count typos.
    allow_typos = allow_typos or combined # want to replace with whether to count typos in the initial computation.
    total = 0
    lnum = 0
    num = 0
    lines = range(1, len(lyrics)+1)
    if index:
        lines = index
    for line in lyrics:
        lnum += 1
        try:
            errs = tool_errors(line, parser=parser, allow_typos=allow_typos)
        except:
            print("error occurred in line :", lnum)
            continue
        else:
            num += 1
            
            total += errs
            if combined:
                total -= lang_typos(line)

            print("file", filename, "line", lnum, ":", lines[lnum-1], " ; total errors:", total, "in", num, "lines")

    return total / len(lyrics)


def lang_typos(line):
    """
    Computes number of typos in a line of lyrics based on language_check parser
    :param line: line of lyrics represented as string value, str
    :return: number of typos, int
    """
    tool = language_check.LanguageTool('en-US')
    matches = tool.check(line)
    typos = [match for match in matches if match.category == 'Possible Typo' or match.category == 'Possible Typos']
    return len(typos)


def get_grammar_score(filename, allow_typos, parser, combined, sample_size = None):
    """
    Returns grammar score of the given file based on score method
    :param filename: name of file containing lyrics, str
    :param allow_typos: a boolean value specifying whether to include typos, bool
    :param parser: parser instance, GingerIt; None for LanguageTool
    :param combined: a boolean value specifying whether to combine tools, bool
    :param sample_size: number of lines that should be randomly evaluated. Entire lyrics is chosen if equals None, int
    :return: score, float
    """
    lines = None
    with open(filename, "r") as f:
        lyrics = f.readlines()
        if sample_size and sample_size < len(lyrics):
            lines = random.sample(range(len(lyrics)), sample_size)
            lyrics = list(map(lambda i: lyrics[i], lines))
        
    score = mean_error(lyrics, allow_typos=allow_typos, parser=parser, combined=combined, filename=filename, index=lines)
    print(filename, "has mean grammatical error ", score)
    return score


ginger_parser = GingerIt()
#print(get_grammar_score('data/50-cent.txt', allow_typos=True, parser=ginger_parser, combined=False))
"""
freddie: allow_typos=False, 0.29 / 0.29 with and without consideration of ' not'
50-cent: allow_typos=False, 0.56 / 0.67 with and without consideration of ' not'
"""




