"""
Lyrer lyrics package __init__

package for getting lyrics from external APIs

@category   Utility
@version    $ID: 1.1.1, 2015-06-30 17:00:00 CST $;
@author     KMR
@licence    GNU GPL v.3
"""

import os
import yaml

DIR = os.path.dirname(os.path.realpath(__file__))
config = yaml.safe_load(open("{}/lyrics.cfg".format(DIR)))
__all__ = config["modules"]
