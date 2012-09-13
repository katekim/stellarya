import os

from PyQt4.QtCore import *
from sleepy.extract import *

class Posix:

    @property
    def firefoxConfigDir(self):
        return os.path.join(
            unicode(QDir.homePath()), ".mozilla", "firefox")

    @property
    def firefoxPathCandidates(self):
        return L(
            "/usr/bin/firefox",
            "/usr/local/bin/firefox",
            "/opt/bin/firefox",
            "/opt/local/bin/firefox",
            )


class Win:

    @property
    def firefoxConfigDir(self):
        return os.path.join(
            unicode(QDir.homePath()), "Application Data", "Mozilla", "Firefox")

    @property
    def firefoxPathCandidates(self):
        return L(
            r"C:\Program Files\Mozilla Firefox"
            )

OsSpecific = Win() if os.name == "nt" else \
             Posix()

__all__ = ["OsSpecific"]
