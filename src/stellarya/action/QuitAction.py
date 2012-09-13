from PyQt4.QtGui import *

from Action import *
import stellarya

class QuitAction(Action):

    def __init__(self):
        Action.__init__(self)

        style = stellarya._.app.style()
        self.setText("&Ouit")
        self.setIconText("Ouit")
        self.setToolTip("Quit")

    def __call__(self):
        stellarya._.app.quit()
