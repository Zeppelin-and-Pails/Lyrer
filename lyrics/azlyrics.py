"""
azlyrics

Gets the lyrics for a song using the azlyrics website

@category   silly
@version    $ID: 1.1.1, 2015-06-30 17:00:00 CST $;
@author     KMR
@licence    GNU GPL v.3
"""
__version__ = "1.1.1"

import requests
from bs4 import BeautifulSoup

class azlyrics:
    config = None

    def __init__(self, conf):
        self.config = conf
        print "azlyrics initialised successfully"

    def removeSpaces(self, text):
        text = text.replace(" ", "").replace("&","")
        text = text.replace(".","")
        return text.lower()

    def getLyrics(self, artist, song):
        lyrics = None

        try:
            headers = {
                'User-Agent': 'My User Agent 1.0'
            }

            # build the uri
            uri = self.config['url'].format(self.removeSpaces(song), self.removeSpaces(artist))

            # request the page
            r = requests.get(uri, headers=headers)
            # make it into a delicious soup
            soup = BeautifulSoup(r.text)
            # strain the crap out of the soup
            bigDiv = soup.find( 'div', { 'class': 'col-xs-12 col-lg-8 text-center'} )

            lyrics = bigDiv.find('div', {'class': None}).get_text(" ").strip()

        except:
            print "azlyrics failed"

        return lyrics

