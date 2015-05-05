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
        if self.config['debug']:
            if self.config['chartlyrics']:
                print "getLyrics called using ChartLyrics"
            elif self.config['metrolyrics']:
                print "getLyrics called using MetroLyrics"
            
        if self.config['chartlyrics']:
            payload = {'artist': artist, 'song': song}
            r = requests.get(self.config['cluri'], params=payload)
            soup = BeautifulSoup(r.text, "xml")
            
            lyrics = soup.GetLyricResult.Lyric.text.lower()

        elif self.config['metrolyrics']:
            uri = self.config['mluri'].format(self.addDash(song), self.addDash(artist))
            if self.config['debug']:
                print 'requests'
                print uri
            r = requests.get(uri)
            
            if self.config['debug']:
                print 'soup'
            soup = BeautifulSoup(r.text)
            
            if self.config['debug']:
                print 'lyrics'
            lyrics = soup.find( 'div', { 'id': 'lyrics-body-text'} ).get_text(" ").strip()
        
        if self.config['debug']:
            print "getLyrics completed successfully"
        return re.sub(r'[^a-zA-Z0-9\s]', r'', lyrics.lower())

    def getLyricStats(self, lyrics):
        if self.config['debug']:
            print "getLyricStats called"
        total = 0
        details = {}
        words = lyrics.split()
            
        for word in words:
            total += 1
            if word not in details:
                details[word] = {}
                details[word]['count'] = 1
            else:
                details[word]['count'] += 1

        for word in details:
            details[word]['percent'] = (details[word]['count'] / total) * 100

        return details
        
    def addDash(self, undashed):
        return undashed.replace(" ", "-")



