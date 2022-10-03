import pandas as pd
bands_data_parts = [pd.read_csv('data/bands_data/ma_bands_data_' + str(i) + '.csv', index_col=0) for i in range(0, 20)]
bands_data = pd.concat(bands_data_parts, ignore_index=True)
bands_data.to_csv('data/ma_bands_data.csv')
