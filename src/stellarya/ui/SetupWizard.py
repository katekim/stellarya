import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sleepy.extract import *

import UiLoader
import stellarya

class FirefoxLocationPage(QWizardPage):

    def __init__(self):
        QWizardPage.__init__(self)

        self._ui = UiLoader.load("FirefoxLocationPage")
        self._ui.setupUi(self)

        def btnFindClicked():
            dlg = QFileDialog(self)
            if dlg.exec_():
                files = dlg.selectedFiles()
                self._ui._edtPath.setText(files[0])

        self._ui._btnFind.clicked.connect(btnFindClicked)

        self.registerField("location_path", self._ui._edtPath)

    def initializePage(self):
        paths = stellarya.OsSpecific.firefoxPathCandidates.filter(os.path.exists)
        if paths.isEmpty:
            desc = self.tr("""\
Firefox doesn't seem to be installed in standard paths.
Specify a path to Firefox manually.
If you haven't had Firefox installed yet, install it first.""")
        else:
            desc = self.tr("""\
Firefox is found in the location below.
If you want to use another Firefox in a different place, specify the path manually.""")
            self._ui._edtPath.setText(paths[0])

        self._ui._lblDescription.setText(desc)

    def validatePage(self):
        path = self.field("location_path").toString()
        exists = os.path.exists(path)
        if not exists:
            QMessageBox.critical(
                self,
                self.tr("Invalid Path"),
                self.tr("The path you specified doesn't exist."))

        return exists


class ProfileNamePage(QWizardPage):

    InvalidCharacters = r'/\?%*:|"<>'

    def __init__(self):
        QWizardPage.__init__(self)

        self._ui = UiLoader.load("ProfileNamePage")
        self._ui.setupUi(self)

        self._edtName = QLineEdit()
        self.registerField("profile_name", self._edtName)

    def initializePage(self):
        self.__setupToggle()
        self.__setupExistingProfileNames()

    def __setupToggle(self):
        def radNewToggled(on):
            if on:
                self._ui._edtNewProfileName.setEnabled(True)
                self._ui._cmbProfileNames.setEnabled(False)
            else:
                self._ui._edtNewProfileName.setEnabled(False)
                self._ui._cmbProfileNames.setEnabled(True)

        self._ui._radNew.toggled.connect(radNewToggled)

    def __setupExistingProfileNames(self):
        profileFile = os.path.join(
            stellarya.OsSpecific.firefoxConfigDir, "profiles.ini")
        if not os.path.exists(profileFile):
            return

        Li(open(profileFile).readlines()) \
            .filter(_.startswith("Name=")) \
            .map(_.replace("Name=", "").strip()) \
            .forEach(self._ui._cmbProfileNames.addItem)

    def validatePage(self):
        if self._ui._radExisting.isChecked():
            idx = self._ui._cmbProfileNames.currentIndex()
            name = self._ui._cmbProfileNames.itemText(idx)
        else:
            name = self._ui._edtNewProfileName.text()

        valid = Li(self.InvalidCharacters) \
            .map(lambda s: s in name) \
            .forAll(_ == False)
        if not valid:
            QMessageBox.critical(
                self,
                self.tr("Invalid Characters"),
                self.tr("A profile name cannot contain the following characters.\n\n" + self.InvalidCharacters))

            return False

        self._edtName.setText(name)
        return True


class CommandLinePage(QWizardPage):

    def __init__(self):
        QWizardPage.__init__(self)

        self._ui = UiLoader.load("CommandLinePage")
        self._ui.setupUi(self)

        self.registerField("command_line", self._ui._edtCommandLine)

    def initializePage(self):
        self._ui._edtCommandLine.setText(
            stellarya._.preferences["command_line"])


class SetupWizard(QWizard):

    def __init__(self, parent):
        QWizard.__init__(self, parent)

        self.addPage(FirefoxLocationPage())
        self.addPage(ProfileNamePage())
        self.addPage(CommandLinePage())

        self.accepted.connect(self.__accepted)

    def __accepted(self):
        p = stellarya._.preferences
        p["firefox_location"] = unicode(self.field("location_path").toString())
        p["profile_name"] = unicode(self.field("profile_name").toString())
        p["command_line"] = unicode(self.field("command_line").toString())


__all__ = ["SetupWizard"]
