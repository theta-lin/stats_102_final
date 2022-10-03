from metal_archives import MetalArchives
import pandas as pd

ma = MetalArchives()

bands = pd.read_csv('ma_bands.csv', index_col=0)

def get_song_chunk(chunk_num, chunk_id):
    print('Chunk:', chunk_id, '/', chunk_num)

    chunk_size = bands.shape[0] // chunk_num
    begin = chunk_size * chunk_id
    end = begin + chunk_size
    if (chunk_id == chunk_num - 1):
        end = bands.shape[0]

    songs = list()
    for row in range(begin, end):
        print('Band:', row - begin, '/', end - begin, '-', int((row - begin) / (end - begin) * 100) , '%          ', end='\r')
        songs += ma.search_song(band_name=bands.loc[row, 'name'])
    return songs

chunk_num = int(input('Number of chunks:'))
chunk_id = int(input('ID of current chunk:'))
songs = pd.DataFrame(get_song_chunk(chunk_num, chunk_id))
songs.to_csv('ma_songs_' + str(chunk_id) + '.csv')
