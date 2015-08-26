"""
lyrics

Gets the lyrics for a song using the chartlyrics website

@category   silly
@version    $ID: 1.1.1, 2015-06-30 17:00:00 CST $;
@author     KMR
@licence    GNU GPL v.3
"""
__version__ = "1.1.1"

import os
import yaml

class lyrics:
    config = None

    def __init__(self):
        DIR = os.path.dirname(os.path.realpath(__file__))
        self.config = yaml.safe_load(open("{}/lyrics.cfg".format(DIR)))

    def getModules(self):
        return self.config["modules"]