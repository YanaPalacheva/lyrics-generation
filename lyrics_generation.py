from lyrics_generator import LyricsGenerator


artist = 'freddie-mercury'
genre = 'pop'

# params
depth = 4
max_syllables = 12

lyrics_gen = LyricsGenerator(max_syllables, artist, depth, old=True)
lyrics_gen.training_phase()
lyrics_gen.generating_phase()
