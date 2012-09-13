import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import stellarya

class Stellarya:

    def __guiMain(self):
        stellarya._.setup()
        stellarya._.mainDialog = stellarya.ui.MainDialog()
        stellarya._.mainDialog.show()
        stellarya._.launcher.startMonitoring()

    def main(self):
        exitStatus = 0
        try:
            QTimer.singleShot(0, self.__guiMain)
            exitStatus = stellarya._.app.exec_()
        except:
            import traceback
            traceback.print_exc()
            exitStatus = 1

        return exitStatus


if __name__ == "__main__":
    sys.exit(Stellarya().main())
