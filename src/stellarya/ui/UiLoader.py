import os

from PyQt4.uic import *

import stellarya

def load(name):
    fp = stellarya._.resourceLoader.getfp("ui/" + name + ".ui")
    cls = loadUiType(fp)[0]
    return cls()
