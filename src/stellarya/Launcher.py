import subprocess

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import stellarya

class Stopped(QObject):

    @property
    def text(self):
        return self.tr("stopped")


class Running(QObject):

    def __init__(self, pid=-1):
        QObject.__init__(self)
        self._pid = pid

    @property
    def text(self):
        return self.tr("running") if self._pid < 0 else \
               unicode(self.tr("running (PID: %d)")) % self._pid


class Launcher(QObject):

    Stopped, Running = Stopped(), Running()

    statusChanged = pyqtSignal(QObject)

    def __init__(self):
        QObject.__init__(self)

        self._proc = None
        self._status = self.Stopped

    def __timeout(self):
        try:
            dlg = stellarya._.mainDialog
            if self._proc:
                if self._proc.poll() is None:
                    status1 = Running(self._proc.pid)
                else:
                    status1 = self.Stopped
                    self._proc = None
            else:
                status1 = self.Stopped

            if status1 != self._status:
                self._status = status1
                self.statusChanged.emit(self._status)
        finally:
            QTimer.singleShot(200, self.__timeout)

    def startMonitoring(self):
        self.__timeout()

    def run(self):
        tmpl = stellarya._.preferences["command_line"]
        cmd = tmpl % {
            "firefox" : stellarya._.preferences["firefox_location"],
            "profile" : stellarya._.preferences["profile_name"]}
        self._proc = subprocess.Popen(cmd, shell=True)


__all__ = ["Launcher"]
