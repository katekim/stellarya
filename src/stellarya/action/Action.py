from PyQt4.QtGui import *

import stellarya

class Action(QAction):

    def __init__(self):
        QAction.__init__(self, None)
        self.triggered.connect(self)

    def __call__(self):
        raise NotImplemented("__call__")
