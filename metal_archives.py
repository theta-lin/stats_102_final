from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

def get_random_user_agent():
    # you can also import SoftwareEngine, HardwareType, SoftwareType, Popularity from random_user_agent.params
    # you can also set number of user agents required by providing `limit` as parameter

    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value,
                         OperatingSystem.LINUX.value]

    user_agent_rotator = UserAgent(software_names=software_names,
                                   operating_systems=operating_systems,
                                   limit=100)

    return user_agent_rotator.get_random_user_agent()

from requests_cache import CachedSession
from datetime import timedelta
from lxml import html
import re
import time

class MetalArchives:
    session = CachedSession(backend='memory',
                            expire_after=timedelta(hours=1))
    site_url = 'https://www.metal-archives.com/'
    url_search_songs = 'search/ajax-advanced/searching/songs?'
    url_search_bands = 'search/ajax-advanced/searching/bands?'
    url_lyrics = 'release/ajax-view-lyrics/id/'
    lyrics_not_available = '(lyrics not available)'
    lyric_id_re = re.compile(r'id=.+[a-z]+.(?P<id>\d+)')
    band_name_re = re.compile(r'title="(?P<name>.*)\"')
    tags_re = re.compile(r'<[^>]+>')
    genres = ["black", "death", "doom", "stoner", "sludge", "electronic",
              "industrial", "experimental", "avant-garde", "folk", "viking",
              "pagan", "gothic", "grindcore", "groove", "heavy", "metalcore",
              "deathcore", "power", "progressive", "speed", "symphonic",
              "thrash"]

    @staticmethod
    def get_band_data(url):
        result = {}

        response = None
        for attempt in range(0, 10):
            time.sleep(3)

            try:
                response = MetalArchives.session.get(url,
                                                     headers={'User-Agent': get_random_user_agent()})
            except:
                print('Error, retrying...', attempt, '                    ', end='\r')
                continue

            break

        if response == None: return None

        tree = html.fromstring(response.content)
        result["name"] = \
            tree.xpath('//*[@id="band_info"]/h1/a/text()')
        result["url"] = \
            tree.xpath('//*[@id="band_info"]/h1/a/@href')
        result["genre"] = \
            tree.xpath(".//*[@id='band_stats']/dl[2]/dd[1]/text()")
        result["theme"] = \
            tree.xpath(".//*[@id='band_stats']/dl[2]/dd[2]/text()")
        result["label"] = \
            tree.xpath(".//*[@id='band_stats']/dl[2]/dd[3]/text()")
        result["country"] = \
            tree.xpath(".//*[@id='band_stats']/dl[1]/dd[1]/a/text()")
        result["location"] = \
            tree.xpath(".//*[@id='band_stats']/dl[1]/dd[2]/text()")
        result["status"] = \
            tree.xpath(".//*[@id='band_stats']/dl[1]/dd[3]/text()")
        result["date"] = \
            tree.xpath(".//*[@id='band_stats']/dl[1]/dd[4]/text()")
        years_active = \
            tree.xpath(".//*[@id='band_stats']/dl[3]/dd/text()")
        result["years"] = years_active

        for r in result.keys():
            if isinstance(result[r], list) and len(result[r]) == 1:
                result[r] = result[r][0]
            elif isinstance(result[r], list) and len(result[r]) == 0:
                result[r] = None
            if isinstance(result[r], str) and result[r] == 'N/A':
                result[r] = None
            #if r == "years":
            #    if "," in result[r]:
            #        years = result[r].split(",")
            #        result[r] = [y.rstrip().lstrip() for y in years]
            #    else:
            #        result[r] = [result[r].rstrip().lstrip()]
            if r == 'years' and result[r] is not None:
                result[r] = ''.join([y.strip().replace('\n', '') for y in result[r]])
            if r == "theme" and result[r] is not None:
                result[r] = result[r].split(",")
        return result

    def search_song(self, song_title="", band_name="", album_type="any",
                    excluded_album_types=None):

        excluded_album_types = excluded_album_types or []
        index = 0
        params = dict(bandName=band_name, songTitle=song_title, iDisplayStart=index)
        url = self.site_url + self.url_search_songs

        num = None
        num_display = None
        for attempt in range(0, 10):
            time.sleep(3)

            try:
                response = self.session.get(url, params=params,
                                headers={'User-Agent': get_random_user_agent()}).json()
                num = response['iTotalRecords']
                num_display = response['iTotalDisplayRecords']

            except:
                print('Error, retrying...', attempt, '                    ', end='\r')
                continue

            break

        if num == None: return list()

        result = list()
        while index < num:
            index += num_display

            for attempt in range(0, 10):
                time.sleep(3)

                try:
                    params['iDisplayStart'] = index
                    songs = self.session.get(url, params=params,
                                        headers={'User-Agent': get_random_user_agent()}).json()['aaData']

                    for song in songs:
                        if album_type != "any":
                            if song[2] != album_type:
                                continue
                        if song[2] in excluded_album_types:
                            continue
                        data = {"album_url": song[0][
                                             song[0].find('href="') + 6:song[0].find(
                                                 '" title=')],
                                "band_name": song[0][
                                             song[0].find('>') + 1:song[0].find('</a')],
                                "album_name": song[1][
                                              song[1].find('">') + 2:song[1].find('</a')],
                                "album_type": song[2],
                                "song_name": song[3],
                                "song_id": self.lyric_id_re.search(song[4]).group("id")}
                        result.append(data)

                    print("Song: ", index, '/', num, '-', int(index / num * 100) , '%          ', end='\r')

                except:
                    print('Error, retrying...', attempt, index, '/', num, '-', int(index / num * 100) , '%          ', end='\r')
                    continue

                break

        return result

    def search_band(self, band_name="", genre=""):
        index = 0
        params = dict(bandName=band_name, genre=genre, iDisplayStart=index)
        url = self.site_url + self.url_search_bands

        num = None
        num_display = None
        for attempt in range(0, 10):
            time.sleep(3)

            try:
                response = self.session.get(url, params=params,
                                headers={'User-Agent': get_random_user_agent()}).json()
                num = response['iTotalRecords']
                num_display = response['iTotalDisplayRecords']

            except:
                print('Error, retrying...', attempt, '                    ', end='\r')
                continue

            break

        if num == None: return list()

        result = list()
        while index < num:
            index += num_display

            for attempt in range(0, 10):
                time.sleep(3)

                try:
                    params['iDisplayStart'] = index
                    bands = self.session.get(url, params=params,
                                        headers={'User-Agent': get_random_user_agent()}).json()['aaData']

                    for band in bands:
                        data = {
                            "url": band[0][band[0].find('href="') + 6:band[0].find('">')],
                            "name": band[0][band[0].find('">') + 2:band[0].find('</a>')],
                            "genre": band[1],
                            "country": band[2]}
                        result.append(data)

                    print("Band: ", index, '/', num, '-', int(index / num * 100) , '%          ', end='\r')

                except:
                    print('Error, retrying...', attempt, index, '/', num, '-', int(index / num * 100) , '%          ', end='\r')
                    continue

                break

        return result

    def get_lyrics_by_song_id(self, song_id):
        url = self.site_url + self.url_lyrics + song_id

        data = None
        for attempt in range(0, 10):
            try:
                data = self.session.get(url,
                                    headers={'User-Agent': get_random_user_agent()})

            except:
                print('Error, retrying...', attempt, '                    ', end='\r')
                continue

            break

        if data == None: return None

        lyrics = self.tags_re.sub('', data.text.strip())
        return lyrics
