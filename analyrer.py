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
import json
import requests
from bs4 import BeautifulSoup

class analyrer:
    config = None

    def __init__(self, conf):
        self.config = conf
        if self.config['debug']:
            print "Analyrer initialised successfully"

    def getLyrics(self, artist, song):
        lyrics = self.checkCache(self.addDash(artist), self.addDash(song))

        if not lyrics:
            for source in self.config['lyric_sources']:
                config = self.config['lyric_sources'][ source ]

                if config['type'] == 'scrape':
                    uri = config['uri'].format(self.addDash(song), self.addDash(artist))
                    # request the page
                    r = requests.get(uri)
                    # make it into a delicious soup
                    soup = BeautifulSoup(r.text)
                    # strain the crap out of the soup

                    lyrics = soup.find( 'div', { 'id': 'lyrics-body-text'} )
                    if lyrics:
                        lyrics = str( lyrics ).replace('<br>', '\n ')
                        lyrics = lyrics.replace('<br/>', '.\n ')
                        lyrics = lyrics.replace('<p class="verse">', ' ')
                        lyrics = lyrics.replace('</p>', '.\n ')
                        lyrics = lyrics.replace('</div>', ' ')
                        lyrics = lyrics.replace('<div id="lyrics-body-text">', ' ')

                if config['type'] == 'api':
                    # build a payload for the get params
                    payload = {'artist': artist, 'song': song}
                    # request the xml
                    r = requests.get(config['uri'], params=payload)
                    # make it into a soup
                    soup = BeautifulSoup(r.text, "xml")
                    # get the bit we actually want
                    lyrics = soup.GetLyricResult.Lyric.text

                if lyrics:
                    print "Success from {}".format(source)
                    self.writeCache(self.addDash(artist), self.addDash(song), lyrics)
                    break
        else:
            if self.config['debug']:
                print "Using lyrics from cache"

        if self.config['debug']:
            print "getLyrics completed successfully"

        return {'formated': re.sub(r'[^a-zA-Z0-9 ]', r'', lyrics.lower()), 'raw': lyrics}

    def getLyricStats(self, lyrics):
        if self.config['debug']:
            print "getLyricStats called"
        # setup some stuff
        total = 0
        details = {}
        details['words'] = {}

        # split up the lyrics into words
        words = lyrics['formated'].split()
        # check each one, luck songs aren't that long
        for word in words:
            if word not in details['words']:
                total += 1
                details['words'][word] = {}
                details['words'][word]['count'] = 1
            else:
                details['words'][word]['count'] += 1

        for word in details['words']:
            details['words'][word]['percent'] = (details['words'][word]['count'] / len(words)) * 100

        details['total_words'] = len(words)
        details['unique_words'] = total

        details['readable'] = json.loads( self.getReadable(lyrics['raw']) )

        return details

    def addDash(self, undashed):
        return undashed.replace(" ", "-")

    def checkCache(self, artist, song):
        data = ""
        try:
            with open ("{}/lyrics-{}-{}".format(self.config['cachePath'], artist, song), "r") as myfile:
                data=myfile.read()
        except IOError as err:
            if err.errno == 2:
                pass

        return data

    def writeCache(self, artist, song, lyrics):
        with open ("{}/lyrics-{}-{}".format(self.config['cachePath'], artist, song), "w+") as myfile:
            myfile.write(lyrics)

    def getReadable(self, lyrics):
        if self.config['debug']:
            print "getReadable called"

        data = {'text': lyrics }
        r = requests.post(self.config['gombert'], data=data)

        return r.text
