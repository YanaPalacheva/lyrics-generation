from lyrics_generator import LyricsGenerator
from utils import split_file
from preprocessing import create_rhymescheme
from evaluation.rhyme import rhyme_score
from ui import open_gui


def generate(ident, prms):
    lyrics_gen = LyricsGenerator(ident, prms, syllable_rhyme=False)
    lyrics_gen.training_phase()
    lyrics = lyrics_gen.generating_phase()
    return lyrics


def user_generation(idents, prms):
    with open('data/user-lyrics.txt', 'w') as outfile:
        for ident in idents:
            with open(f'data/{ident}.txt') as infile:
                for line in infile:
                    outfile.write(line)
    return generate('user-lyrics', prms)


def user_evaluation():
    create_rhymescheme('user-lyrics', syllable_rhyme=False, generated=True)
    return evaluate('user-lyrics', syllable_rhyme=False, generated=True)


# evaluation
def evaluate(ident, syllable_rhyme=True, generated=False):
    if generated:
        gen = '_generated'
    else:
        gen = ''
    if syllable_rhyme:
        syl = '.syl'
    else:
        syl = ''
    endings = split_file(f'schemes/{ident}{gen}{syl}.schemes')
    return rhyme_score(endings)


# identifier = 'enya'
# # params
# params = {'depth': 4, 'max_syllables': 10,
#           'max_overlap': 0.5, 'num_lines': 40}
# generate(identifier, params)

open_gui(user_generation, user_evaluation)

