import pandas as pd
songs_parts = [pd.read_csv('data/songs/ma_songs_' + str(i) + '.csv', index_col=0) for i in range(0, 20)]
songs = pd.concat(songs_parts, ignore_index=True)
songs = songs.dropna(subset='song_name').drop_duplicates().reset_index(drop=True)
songs.to_csv('data/ma_songs.csv')
