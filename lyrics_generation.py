from lyrics_generator import LyricsGenerator
from utils import split_file
from evaluation.rhyme import rhyme_score

# score (>3-syllable lines considered)
mean_syls = {'50-cent': 11, 'elvis-presley': 9, 'freddie-mercury': 9, 'evanescence': 8,
             'enya': 7, 'frank-sinatra': 9, 'depeche-mode': 7, 'ed-sheeran': 9, 'david-bowie': 8,
             'hip-hop': 11, 'folk-country': 9, 'jazz': 9, 'rock': 9, 'electronic': 7, 'pop': 9}

identifier = 'david-bowie'
# params
params = {'depth': 4, 'max_syllables': 10,
          'max_overlap': 0.5, 'gen_lyrics_len': 40}

lyrics_gen = LyricsGenerator(identifier, params, syllable_rhyme=True)
# lyrics_gen.training_phase()
lyrics_gen.generating_phase()

# evaluation
# def evaluate(ident, old=False):
#     if old:
#         endings = split_file(f'schemes/{ident}.rhymes')
#     else:
#         endings = split_file(f'schemes/{ident}.schemes')
#     return rhyme_score(endings)
#
#
# iden = 'depeche-mode'
# print(evaluate(iden))


