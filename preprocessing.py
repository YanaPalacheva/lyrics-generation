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
    df = pd.read_csv('lyrics.csv')
    saved_column = df.loc[df['artist'] == artist, ['lyrics']]
    saved_column = saved_column.lyrics
    saved_column = [song for song in saved_column if type(song) == str]

    saved_column = clean_input(saved_column)

    with open('data/' + file, "a", encoding='utf-8') as f:
        for song in saved_column:
            f.write(song)


def create_rhymescheme(identifier, syllable_rhyme, generated=False):
    if syllable_rhyme:
        rhymer = RhymerSyl(identifier, generated)
    else:
        rhymer = RhymerEnd(identifier, generated)
    rhymer.create_rhymescheme()


def mean_syllables(target_list):
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
create_rhymescheme('freddie-mercury', syllable_rhyme=False, generated=False)

# syls = mean_syllables(artists)
# # syls = mean_syllables(genres.keys())
# print(syls)



