import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sleepy.extract import *

import stellarya
import UiLoader

class Setup(QObject):

    def __init__(self, parent):
        QObject.__init__(self)

        self._parent = parent
        self._ui = self._parent._ui

    def setup(self):
        #self.__setupMenu()
        self.__setupSignalsAndSlots()
        self.__setupPreferences()
        self.__setupAbout()
        self.__setupRun()

    def __setupMenu(self):
        self._ui._menuFile.addAction(
            stellarya.action.QuitAction())

    def __setupSignalsAndSlots(self):
        stellarya._.preferences.changed.connect(
            self._parent.preferenceChanged)
        stellarya._.preferences.emitAll()

        stellarya._.launcher.statusChanged.connect(
            self._parent.runningStatusChanged)
        self._parent.runningStatusChanged(stellarya._.launcher.Stopped)

    def __setupPreferences(self):

        def btnFirefoxLocationClicked():
            dlg = QFileDialog(self._parent)
            if dlg.exec_():
                files = dlg.selectedFiles()
                stellarya._.preferences["firefox_location"] = unicode(files[0])

        self._ui._btnFirefoxLocation.clicked.connect(btnFirefoxLocationClicked)

        def btnProfileNameClicked():
            name, successful = QInputDialog.getText(
                self._parent,
                self.tr("Profile Name"),
                self.tr("Enter a name of profile you want to launch Firefox with."))
            if successful:
                stellarya._.preferences["profile_name"] = unicode(name)

        self._ui._btnProfileName.clicked.connect(btnProfileNameClicked)

        def btnCommandLineClicked():
            cmdline, successful = QInputDialog.getText(
                self._parent,
                self.tr("Command Line"),
                self.tr("""\
Enter command line arguments used for Firefox to start.

"%(firefox)s" and "%(profile)s" will be replaced with
Firefox executable path and profile name respectively."""))
            if successful:
                stellarya._.preferences["command_line"] = unicode(cmdline)

        self._ui._btnCommandLine.clicked.connect(btnCommandLineClicked)

        def btnWizardClicked():
            wizard = stellarya.ui.SetupWizard(self._parent)
            wizard.show()

        self._ui._btnWizard.clicked.connect(btnWizardClicked)

    def __setupAbout(self):
        self._ui._lblVersion.setText(
            "Stellarya version %s" % stellarya.versionStr)

    def __setupRun(self):
        self._ui._btnRun.clicked.connect(
            stellarya._.launcher.run)



class MainDialog(QDialog):

    def __init__(self):
        QDialog.__init__(self)
        self._ui = UiLoader.load("MainDialog")
        self._ui.setupUi(self)
        Setup(self).setup()

    def preferenceChanged(self, qKey):
        sKey = str(qKey)
        value = stellarya._.preferences[sKey]

        if sKey == "firefox_location":
            self._ui._lblFirefoxLocation.setText(value)
        elif sKey == "profile_name":
            self._ui._lblProfileName.setText(value)
        elif sKey == "command_line":
            self._ui._lblCommandLine.setText(value)

    def runningStatusChanged(self, status):
        if status == stellarya._.launcher.Stopped:
            self._ui._btnRun.setEnabled(True)
        elif status == stellarya._.launcher.Running:
            self._ui._btnRun.setEnabled(False)

        self._ui._lblRunningStatus.setText(status.text)


__all__ = ["MainDialog"]
