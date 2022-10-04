from metal_archives import MetalArchives
import pandas as pd

ma = MetalArchives()

songs = pd.read_csv('ma_songs_essential.csv', index_col=0)

def get_lyrics_chunk(chunk_num, chunk_id):
    print('Chunk:', chunk_id, '/', chunk_num)

    chunk_size = songs.shape[0] // chunk_num
    begin = chunk_size * chunk_id
    end = begin + chunk_size
    if (chunk_id == chunk_num - 1):
        end = songs.shape[0]

    lyrics = list()
    for row in range(begin, end):
        print('Song:', row - begin, '/', end - begin, '-', int((row - begin) / (end - begin) * 100), '%          ', end='\r')
        lyrics.append(ma.get_lyrics_by_song_id(str(songs.loc[row, 'song_id'])))
    return range(begin, end), lyrics

chunk_num = int(input('Number of chunks:'))
chunk_id = int(input('ID of current chunk:'))
index, values = get_lyrics_chunk(chunk_num, chunk_id)
lyrics = pd.DataFrame(values, index=index)
lyrics.to_csv('ma_lyrics_' + str(chunk_id) + '.csv')
