"""
chartlyrics

Gets the lyrics for a song using the chartlyrics website

@category   silly
@version    $ID: 1.1.1, 2015-06-30 17:00:00 CST $;
@author     KMR
@licence    GNU GPL v.3
"""
__version__ = "1.1.1"

import requests
from bs4 import BeautifulSoup

class chartlyrics:
    config = None

    def __init__(self, conf):
        self.config = conf
        print "chartlyrics initialised successfully"

    def getLyrics(self, artist, song):
        # build a payload for the get params
        payload = {'artist': artist, 'song': song}
        # request the xml
        r = requests.get(self.config['url'], params=payload)
        # make it into a soup
        soup = BeautifulSoup(r.text, "xml")
        # get the bit we actually want
        lyrics = soup.GetLyricResult.Lyric.text