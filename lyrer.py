"""
lyrer - lyric analysis api

Get stats for song lyrics

@category   silly
@version    $ID: 1.1.1, 2015-05-04 17:00:00 CST $;
@author     KMR
@licence    http://www.wtfpl.net
"""
__version__ = "1.1.1"

#Import some stuff
import analyrer
import os
import yaml

from flask import Flask, jsonify

#Work out where we are
DIR = os.path.dirname(os.path.realpath(__file__))
#Get the config
config = yaml.safe_load(open("{}/lyrer.cfg".format(DIR)))

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
        details = analyr.getLyricStats(lyrics)

        return jsonify(details)

app.debug = True if config['debug'] else False
app.run(host=config['host'], port=config['port'])
