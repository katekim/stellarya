import os
import sys
import zipfile

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class BaseResourceLoader:

    def get(self, path):
        return self.getfp(path).read()

    def getIcon(self, path):
        img = QImage.fromData(self.get(path), "PNG")
        pix = QPixmap.fromImage(img)
        return QIcon(pix)

    def getPixmap(self, path):
        img = QImage.fromData(self.get(path), "PNG")
        return QPixmap.fromImage(img)


class FileSystemResourceLoader(BaseResourceLoader):

    def __init__(self):
        self._basedir = os.path.dirname(os.path.dirname(__file__))

    def getfp(self, path):
        return open(os.path.join(self._basedir, path))


class ZipResourceLoader(BaseResourceLoader):

    def __init__(self):
        self._zip = zipfile.ZipFile("src.zip")

    def getfp(self, path):
        return self._zip.open(path)


if hasattr(sys, "frozen"):
    ResourceLoader = ZipResourceLoader
else:
    ResourceLoader = FileSystemResourceLoader


__all__ = ["ResourceLoader"]
