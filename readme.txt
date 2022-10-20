Data is stored separately on https://duke.box.com/s/xdtvc5unf555bgarmzopb42028nppygb
Please download the "stats\_102\_final\_data" folder, rename it as "data", and put it in the project root folder.

The run order is follows, it is highly advised not to run the scraping and merging scripts and notebooks:
1. Run ma_scraper.ipynb, scrape basic bands data
2. Run ma_scraper.ipynb, scrape more detailed bands data
3. Run merge.ipynb, merge bands data
4. Run ma_scraper.ipynb, scrape songs
5. Run merge.ipynb, merge songs
6. Run songs_cleaning.ipynb
7. Run ma_scraper.ipynb, scrape lyrics
8. Run merge.ipynb, merge lyrics
9. Run lyrics_cleaning.ipynb
10. Run bands_basic.ipynb
11. Run lyrics_basic.ipynb
12. Run bands_clustering.ipynb
13. Run bands_prediction.ipynb
