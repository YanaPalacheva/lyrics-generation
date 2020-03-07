from gingerit.gingerit import GingerIt

import os

import csv

from grammar_evaluation_ import get_grammar_score


def evaluate_grammar(evaluation_dir, results_dir, results_name, allow_typos, parser, combined, sample_size):

    """
    Evaluate grammar of lyrics in a given folder

    Iterates through all files in the evaluation directory, and prints their grammaticality scores line by line in a text file in a new results directory

    :param evaluation_dir: name of directory containing (generated) lyrics that need to be evaluated
    :param results_dir: name of directory to place output text file containing results of grammatical evaluation of files in the evaluation directory
    :param results_name: the name of the text file containing the results of grammatical evaluation
    :param allow_typos: a boolean value specifying whether to include typos, bool
    :param parser: parser instance, GingerIt; None for LanguageTool
    :param combined: a boolean value specifying whether to combine tools, bool
    : returns: None
    """

    if not os.path.exists(results_dir):

        os.mkdir(results_dir)


    for filename in os.listdir(evaluation_dir):
        print("begun with", filename)
        score = get_grammar_score(evaluation_dir+filename, allow_typos, parser, combined, sample_size)
        f = open(results_dir+results_name+".txt", "a")
        f.write(filename+" "+str(score)+"\n")

    return 

ginger_parser = GingerIt()

evaluate_grammar('data/', 'grammar scores of originals/',  "another_one", allow_typos=False, parser=ginger_parser, combined=False, sample_size=1000)

#evaluate_grammar('generated_lyrics/', 'grammar scores of generated lyrics/', "generator_evaluation", allow_typos=False, parser=ginger_parser, combined=False, sample_size=1000)





