import pandas as pd
import re
import num2words
import os
from rhymer_syl import RhymerSyl
from rhymer_end import RhymerEnd
from utils import split_file, count_syllables

artists = ['50-cent', 'elvis-presley', 'freddie-mercury', 'evanescence', 'enya',
           'frank-sinatra', 'depeche-mode', 'ed-sheeran', 'david-bowie']
genres = {'hip-hop': ['50-cent', 'drake', '2pac'],
          'folk-country': ['enya', 'carter-family', 'emmylou-harris'],
          'jazz': ['frank-sinatra', 'charlie-parker', 'blues-brothers'],
          'rock': ['evanescence', 'the-animals', 'the-doors', 'elvis-presley', 'freddie-mercury', 'david-bowie'],
          'electronic': ['depeche-mode', 'daft-punk', 'caravan-palace'],
          'pop': ['ed-sheeran', 'ariana-grande', 'adele', 'bee-gees']}


def clean_input(songs):
    """
    Prepares lyrics for further processing: removes unusual characters, punctuation,
    verse and chorus declarations; replaces numbers with word equivalents.

    :param songs: list of song lyrics, str[]
    :return: processed list of lyrics, str[]
    """
    for i, song in enumerate(songs):
        # remove all non-alphanumeric and non-space characters
        song = re.sub(r'[^\w\s-]+', '', song)
        # make sure there is always only one space in a row
        song = re.sub(r' +', ' ', song)
        # make sure there are no empty strings
        song = re.sub(r'\n+', '\n', song)
        # remove all spaces at the beginning and end of the line
        song = re.sub(r'(?<=^) +|(?<=\n) +| +(?=\n)| +(?=&)', '', song)
        # remove 'x2', etc. from lyrics
        song = re.sub(r'x\d+', '', song)
        # remove all verse and chorus declarations
        song = re.sub(r'\n[vV]erse.+(?=\n)|\n[cC]horus.+(?=\n)', '', song)
        # replace all numbers with their word equivalent
        song = re.sub(r"(\d+)", lambda x: num2words.num2words(int(x.group(0))), song)
        songs[i] = song
    return songs


def create_artist_file(file, artist):
    """
    Extracts artist data from MetroLyrics dataset and writes it into a file.

    :param file: target file name for appending the artist lyrics, str
    :param artist: artist name (as it is in the dataset), str
    """
    df = pd.read_csv('lyrics.csv')
    saved_column = df.loc[df['artist'] == artist, ['lyrics']]
    saved_column = saved_column.lyrics
    saved_column = [song for song in saved_column if type(song) == str]

    saved_column = clean_input(saved_column)

    with open('data/' + file, "a", encoding='utf-8') as f:
        for song in saved_column:
            f.write(song)


def create_rhymescheme(identifier, syllable_rhyme=False, generated=False):
    """
    Creates a rhyme scheme of all the line endings in lyrics of the given artist.

    :param identifier: name of an artist or a genre, str
    :param syllable_rhyme: True to create a syllable (morpheme-based) rhyme scheme,
                            False to create a letter-based rhyme scheme
    :param generated: True to create scheme for machine generated lyrics, False for actual lyrics
    """
    if syllable_rhyme:
        rhymer = RhymerSyl(identifier, generated)
    else:
        rhymer = RhymerEnd(identifier, generated)
    rhymer.create_rhymescheme()


def average_syllables(target_list):
    """
    Counts average number of syllables in lyrics for a specified artists and/or genres.

    :param target_list: list of identifiers (artist and/or genres), str
    :return: dictionary {identifier: average number of syllables}, dict
    """
    syllables = {}
    for ident in target_list:
        original_bars = split_file(f'data/{ident}.txt')
        count = 0
        excluded = 0
        for line in original_bars:
            syls = count_syllables(line)
            if syls > 3:
                count += syls
            else:
                excluded += 1
        syllables[ident] = count / (len(original_bars) - excluded)
    return syllables


def create_files():
    """
    Creates files for a list of artists and genres from MetroLyrics dataset.
    """
    for artist in artists:
        create_artist_file(artist + '.txt', artist)
    for genre in genres.keys():
        file = genre + '.txt'
        for artist in genres[genre]:
            create_artist_file(file, artist)


dirs = ['data', 'generated_lyrics', 'models', 'rhymes', 'schemes']
for mydir in dirs:
    if not os.path.exists(mydir):
        os.mkdir(mydir)
# create_files()
# create_rhymescheme('freddie-mercury', syllable_rhyme=False, generated=False)

# syls = mean_syllables(artists)
# # syls = mean_syllables(genres.keys())
# print(syls)

# from evaluation.grammar import lang_errors
# lang_errors('We are make soup')
# original_bars = split_file('data/freddie-mercury.txt')
# print(mean_grammatical_error(original_bars[:50]))


