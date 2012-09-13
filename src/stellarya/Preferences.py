import os
import yaml

from PyQt4.QtCore import *

import stellarya

class Preferences(QObject):

    changed = pyqtSignal(str)

    def __init__(self):
        QObject.__init__(self)

        self._data = {}

    @property
    def _cfgpath(self):
        return os.path.join(stellarya._.confdir, "stellarya.cfg")

    def load(self):
        self._data = yaml.load(
            stellarya._.resourceLoader.getfp("default.yaml"))

        if not os.path.exists(self._cfgpath):
            return

        try:
            existingData = yaml.load(open(self._cfgpath))
        except:
            stellarya._.notifier.abort("""\
Your preference data seems to be collapsed.
Check the preference file or delete it if you want to start with default preferences.

%s
""" % self._cfgpath)

        for k, v in existingData.items():
            self._data[k] = v

    def save(self):
        try:
            yaml.dump(self._data,
                      open(self._cfgpath, "w"),
                      default_flow_style=False,
                      allow_unicode=True)
        except:
            stellarya._.notifier.exc(
                "Failed to save preferences data to %s." % self._cfgpath)

    def emitAll(self):
        for key in self._data:
            self.changed.emit(key)

    def __getitem__(self, sKey):
        return self._data[sKey]

    def __setitem__(self, sKey, value):
        if sKey not in self._data:
            stellarya._.notifier.syserror(
                "%s is not a valid preference key." % sKey)

        if type(value) not in (int, long, float, str, unicode, tuple, list, dict):
            stellarya._.notifier.syserror(
                "%s of type %s is not a valid type." % (sKey, type(sKey)))

        self._data[sKey] = value
        self.save()
        self.changed.emit(sKey)
