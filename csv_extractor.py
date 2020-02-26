import pandas as pd
import re
import num2words


def clean_input(songs):
    for i, song in enumerate(songs):
        # remove all non-alphanumeric and non-space characters
        song = re.sub(r'[^\w\s-]+', '', song)
        # make sure there is always only one space in a row
        song = re.sub(r' +', ' ', song)
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


def create_files():
    artists = ['50-cent', 'elvis-presley', 'freddie-mercury', 'evanescence', 'enya',
               'frank-sinatra', 'depeche-mode', 'ed-sheeran', 'david-bowie']
    for artist in artists:
        create_artist_file(artist + '.txt', artist)

    genres = {'hip-hop': ['50-cent', 'drake', '2pac'],
              'folk-country': ['enya', 'carter-family', 'emmylou-harris'],
              'jazz': ['frank-sinatra', 'charlie-parker', 'blues-brothers'],
              'rock': ['evanescence', 'the-animals', 'the-doors', 'elvis-presley', 'freddie-mercury', 'david-bowie'],
              'electronic': ['depeche-mode', 'daft-punk', 'caravan-palace'],
              'pop': ['ed-sheeran', 'ariana-grande', 'adele', 'bee-gees']}
    for genre in genres.keys():
        file = genre + '.txt'
        for artist in genres[genre]:
            create_artist_file(file, artist)

create_files()