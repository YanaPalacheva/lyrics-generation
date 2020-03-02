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
        nontypos = [err for err in errors if err['definition']] # and not err['definition'].endswith(' not')]
    else:
        tool = language_check.LanguageTool('en-US')
        errors = tool.check(line)
        nontypos = [err for err in errors if err.category != 'Possible Typos']
    if allow_typos:
        return len(errors)
    else:
        return len(nontypos)


def mean_error(lyrics, allow_typos=False, parser=None, combined=False):
    """
    Computes average number of grammatical errors in an entire lyrics based on Gingerit parser
    :param lyrics: a list of lyrics lines, str[]
    :param allow_typos: a boolean value specifying whether to include allow_typos, bool
    :param parser: parser instance, GingerIt; None for LanguageTool
    :param combined: a boolean value specifying whether to combine tools, bool
    :return: average number of errors per line, float
    """
    total = 0
    for line in lyrics:
        if parser:
            if combined:
                total += tool_errors(line, allow_typos=True, parser=parser) - lang_typos(line)
            else:
                total += tool_errors(line, parser=parser, allow_typos=allow_typos)
        else:
            total += tool_errors(line, parser=None, allow_typos=allow_typos)

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


def get_grammar_score(filename, allow_typos, parser, combined):
    """
    Returns grammar score of the given file based on score method
    :param filename: name of file containing lyrics, str
    :param allow_typos: a boolean value specifying whether to include typos, bool
    :param parser: parser instance, GingerIt; None for LanguageTool
    :param combined: a boolean value specifying whether to combine tools, bool
    :return: score, float
    """
    with open(filename, "r") as f:
        lyrics = f.readlines()
    score = mean_error(lyrics[:100], allow_typos=allow_typos, parser=parser, combined=combined)
    print(filename, "has mean grammatical error ", score)
    return score


ginger_parser = GingerIt()
print(get_grammar_score('data/50-cent.txt', allow_typos=True, parser=ginger_parser, combined=False))
"""
freddie: allow_typos=False, 0.29 / 0.29 with and without consideration of ' not'
50-cent: allow_typos=False, 0.56 / 0.67 with and without consideration of ' not'
"""




