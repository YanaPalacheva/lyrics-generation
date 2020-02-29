from lyrics_generator import LyricsGenerator
from utils import create_markov_model


artist = 'freddie-mercury'
genre = 'hip-hop'
# genre = 'pop'

# params
depth = 4
max_syllables = 10

lyrics_gen = LyricsGenerator(max_syllables, artist, depth)
lyrics_gen.training_phase()
lyrics_gen.generating_phase()



