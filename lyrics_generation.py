from lyrics_generator import LyricsGenerator
from utils import create_markov_model

# score (>3-syllable lines considered)
mean_syls = {'50-cent': 11, 'elvis-presley': 9, 'freddie-mercury': 9, 'evanescence': 8,
             'enya': 7, 'frank-sinatra': 9, 'depeche-mode': 7, 'ed-sheeran': 9, 'david-bowie': 8,
             'hip-hop': 11, 'folk-country': 9, 'jazz': 9, 'rock': 9, 'electronic': 7, 'pop': 9}

identifier = 'enya'
# params
params = {'depth': 4, 'max_syllables': 10,
          'max_overlap': 0.5, 'gen_lyrics_len': 40}

lyrics_gen = LyricsGenerator(identifier, params, old=True)
# lyrics_gen.training_phase()
lyrics_gen.generating_phase()




