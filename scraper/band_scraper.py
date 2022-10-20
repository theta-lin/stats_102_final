from metal_archives import MetalArchives
import pandas as pd

ma = MetalArchives()
bands_list = ma.search_band()
bands = pd.DataFrame(bands_list)
bands.to_csv('ma_bands.csv')
