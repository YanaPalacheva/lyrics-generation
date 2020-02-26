from lyrics_generator import LyricsGenerator


artist = 'beyonce'
genre = 'pop'

# params
depth = 4
max_syllables = 10

lyrics_gen = LyricsGenerator(max_syllables, artist, depth)
lyrics_gen.training_phase()
lyrics_gen.generating_phase()


