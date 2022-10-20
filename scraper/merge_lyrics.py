import pandas as pd
import csv
lyrics_parts = [pd.read_csv('data/lyrics/ma_lyrics_' + str(i) + '.csv', index_col=0) for i in range(0, 10)]
lyrics = pd.concat(lyrics_parts, verify_integrity=True).rename({'0': 'lyrics'}, axis=1)
songs = pd.read_csv('data/ma_songs_essential.csv', index_col=0)
pd.concat((songs, lyrics), axis=1, verify_integrity=True).to_csv('data/ma_songs_lyrics.csv', quoting=csv.QUOTE_NONNUMERIC)
