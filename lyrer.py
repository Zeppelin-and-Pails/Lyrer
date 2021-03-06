"""
lyrer - lyric analysis api

Get stats for song lyrics

@category   silly
@version    $ID: 1.1.1, 2015-05-04 17:00:00 CST $;
@author     KMR
@licence    GNU GPL v.3
"""
__version__ = "1.1.1"

#Import some stuff
import resource
import analyrer
import os
import yaml

from flask import Flask, jsonify

#Work out where we are
DIR = os.path.dirname(os.path.realpath(__file__))
#Get the config
config = yaml.safe_load(open("{}/lyrer.cfg".format(DIR)))

resource.setrlimit(resource.RLIMIT_NOFILE, (65536, 65536))

#Get an analyrer
analyr = analyrer.analyrer(config)

#Make a Flask app
app = Flask(__name__)

@app.route("/<artist>", methods=['GET'])
@app.route("/<artist>/<songname>", methods=['GET'])
def index(artist, songname=None):
    if(songname == None):
        return 'sup'
    else:
        lyrics = analyr.getLyrics(artist, songname)

        if lyrics:

            if "instrumental" in lyrics['formated'] and len(lyrics['formated']) < 50:
                return "Instrumental song found"

            else:
                details = analyr.getLyricStats(lyrics)
                return jsonify(details)
        else:
            return "Could not gather lyrics"

app.debug = True if config['debug'] else False
app.run(host=config['host'], port=config['port'])
