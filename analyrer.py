"""
analyrer

Gets the lyrics for a song, and does some fudging

@category   silly
@version    $ID: 1.1.1, 2015-02-19 17:00:00 CST $;
@author     KMR
@licence    http://www.wtfpl.net
"""
__version__ = "1.1.1"

import re
import requests
from bs4 import BeautifulSoup

class analyrer:
    config = None
    
    def __init__(self, conf):
        self.config = conf
        if self.config['debug']:
            print "Analyrer initialised successfully"

    def getLyrics(self, artist, song):
        # some caveman debug
        if self.config['debug']:
            if self.config['chartlyrics']:
                print "getLyrics called using ChartLyrics"
            elif self.config['metrolyrics']:
                print "getLyrics called using MetroLyrics"
        
        if self.config['chartlyrics']:
            # build a payload for the get params
            payload = {'artist': artist, 'song': song}
            # request the xml
            r = requests.get(self.config['cluri'], params=payload)
            # make it into a soup
            soup = BeautifulSoup(r.text, "xml")
            # get the bit we actually want
            lyrics = soup.GetLyricResult.Lyric.text

        elif self.config['metrolyrics']:
            # build the uri
            uri = self.config['mluri'].format(self.addDash(song), self.addDash(artist))
            # request the page
            r = requests.get(uri)
            # make it into a delicious soup
            soup = BeautifulSoup(r.text)
            # strain the crap out of the soup
            lyrics = soup.find( 'div', { 'id': 'lyrics-body-text'} ).get_text(" ").strip()
        
        if self.config['debug']:
            print "getLyrics completed successfully"
        return re.sub(r'[^a-zA-Z0-9\s]', r'', lyrics.lower())

    def getLyricStats(self, lyrics):
        if self.config['debug']:
            print "getLyricStats called"
        # setup some stuff
        total = 0
        details = {}
        details['words'] = {}
        
        # split up the lyrics into words
        words = lyrics.split()
        # check each one, luck songs aren't that long
        for word in words:
            if word not in details:
                total += 1
                details['words'][word] = {}
                details['words'][word]['count'] = 1
            else:
                details['words'][word]['count'] += 1

        for word in details['words']:
            details['words'][word]['percent'] = (details['words'][word]['count'] / len(words)) * 100

        details['total_words'] = len(words)
        details['unique_words'] = total
        
        return details
        
    def addDash(self, undashed):
        return undashed.replace(" ", "-")



