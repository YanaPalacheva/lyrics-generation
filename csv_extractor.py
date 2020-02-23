import pandas as pd
df = pd.read_csv('lyrics.csv')
saved_column = df.lyrics
saved_column = [song for song in saved_column if type(song) == str]

with open('beyonce.txt', "a", encoding='utf-8') as f:
    for song in saved_column[:30]:
        f.write(song)
