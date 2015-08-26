"""
metrolyrics

Gets the lyrics for a song using the metrolyrics website

@category   silly
@version    $ID: 1.1.1, 2015-06-30 17:00:00 CST $;
@author     KMR
@licence    GNU GPL v.3
"""
__version__ = "1.1.1"

import requests
from bs4 import BeautifulSoup

class metrolyrics:
    config = None

    def __init__(self, conf):
        self.config = conf
        if self.config['debug']:
            print "metrolyrics initialised successfully"

    def getLyrics(self, artist, song):
        # build the uri
        uri = self.config['mluri'].format(self.addDash(song), self.addDash(artist))
        # request the page
        r = requests.get(uri)
        # make it into a delicious soup
        soup = BeautifulSoup(r.text)
        # strain the crap out of the soup
        lyrics = soup.find( 'div', { 'id': 'lyrics-body-text'} ).get_text(" ").strip()