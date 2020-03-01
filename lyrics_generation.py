from lyrics_generator import LyricsGenerator
from utils import split_file
from evaluation.rhyme import rhyme_score
from ui import open_gui


def generate(ident, prms):
    lyrics_gen = LyricsGenerator(ident, prms, old=True)
    # lyrics_gen.training_phase()
    lyrics = lyrics_gen.generating_phase()
    return lyrics


# evaluation
def evaluate(ident, old=False):
    if old:
        endings = split_file(f'schemes/{ident}.rhymes')
    else:
        endings = split_file(f'schemes/{ident}.schemes')
    return rhyme_score(endings)


identifier = 'enya'
# params
params = {'depth': 4, 'max_syllables': 10,
          'max_overlap': 0.5, 'num_lines': 40}

# generate(identifier, params)

open_gui(generate)

# iden = 'depeche-mode'
# print(evaluate(iden))





