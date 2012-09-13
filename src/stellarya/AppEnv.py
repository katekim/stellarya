import os
import sys
import traceback

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sleepy

from Launcher import *
from Preferences import *
import stellarya

class ErrorNotifier(QObject):

    def abort(self, *args, **kwargs):
        self.exc(*args, **kwargs)
        stellarya._.app.exit(1)

    def error(self, msg, title=None):
        if not title:
            title = self.tr("Error")

        QMessageBox.critical(None, title, msg)

    def syserror(self, msg):
        s = u"%s\n\n%s" % (msg, "".join(traceback.format_stack()))
        self.error(s, self.tr("System Error"))

    def exc(self, msg, title=None):
        if not title:
            title = self.tr("Error")

        s = u"%s\n\n%s" % (msg, traceback.format_exc())
        QMessageBox.critical(None, title, s)


class AppEnv(QObject):

    def __init__(self):
        QObject.__init__(self)

        self.app = QApplication(sys.argv)
        self.confdir = os.getcwd()
        self.launcher = Launcher()
        self.notifier = ErrorNotifier()
        self.preferences = Preferences()
        self.resourceLoader = stellarya.resource.ResourceLoader()

    def setup(self):
        self.preferences.load()


_ = AppEnv()

__all__ = ["_"]
