"""
analyrer

Gets the lyrics for a song, and does some fudging

@category   silly
@version    $ID: 1.1.1, 2015-02-19 17:00:00 CST $;
@author     KMR
@licence    GNU GPL v.3
"""
__version__ = "1.1.1"

import re
import json
import requests
import importlib
from lyrics import lyrics

class analyrer:
    config = None
    sources = None
    lyr = None

    def __init__(self, conf):
        self.config = conf
        self.lyr = lyrics.lyrics()
        self.sources = self.lyr.getModules()

        if self.config['debug']:
            print "Analyrer initialised successfully"

    def getLyrics(self, artist, song):
        toReturn = None
        songLyrics = self.checkCache(self.addDash(artist), self.addDash(song))

        if not songLyrics:
            for module in self.sources:
                lyricModule = importlib.import_module("lyrics.{}".format(module))
                class_ = getattr(lyricModule, module)
                instance = class_(self.lyr.getConfig(module))
                songLyrics = instance.getLyrics(artist, song)

                if songLyrics:
                    self.writeCache(self.addDash(artist), self.addDash(song), songLyrics)
                    break
        else:
            if self.config['debug']:
                print "Using lyrics from cache"

        if self.config['debug']:
            print "getLyrics completed successfully"

        if songLyrics:
            toReturn = {'formated': re.sub(r'[^a-zA-Z0-9 ]', r'', songLyrics.lower()), 'raw': songLyrics}

        return toReturn

    def getLyricStats(self, songLyrics):
        if self.config['debug']:
            print "getLyricStats called"
        # setup some stuff
        total = 0
        details = {}
        details['words'] = {}

        # split up the lyrics into words
        words = songLyrics['formated'].split()
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

        details['readable'] = json.loads( self.getReadable(songLyrics['raw']) )

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

    def writeCache(self, artist, song, songLyrics):
        with open ("{}/lyrics-{}-{}".format(self.config['cachePath'], artist, song), "w+") as myfile:
            myfile.write(songLyrics.encode('UTF-8'))

    def getReadable(self, songLyrics):
        if self.config['debug']:
            print "getReadable called"

        data = {'text': songLyrics }
        r = requests.post(self.config['gombert'], data=data)

        return r.text
