import pandas as pd
df = pd.read_csv('lyrics.csv')
saved_column = df.loc[df['artist'] == 'beyonce', ['lyrics']]
saved_column = saved_column.lyrics
saved_column = [song for song in saved_column if type(song) == str]

with open('beyonce.txt', "a", encoding='utf-8') as f:
    for song in saved_column:
        f.write(song)

