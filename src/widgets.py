

# For logging.
import logging
import logging.config

# For PyQt widgets.
from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class BarLabel(QLabel):
    def __init__(self, number=0, parent=None):

        super().__init__(parent)

        font = QFont("Courier New", 14)
        font.setBold(True)
        self.setFont(font)

        self.setAlignment(Qt.AlignHCenter)

        self.number = number
        self.drawLineAsNum(self.number)

    def clear(self):
        self.drawLineAsNum(0)

    def drawLineAsNum(self, number=0):

        # Seven spaces is '0'.
        text = "       "

        if number == 0:
            text = "       "
        elif number == 6:
            text = "---X---"
        elif number == 7:
            text = "-------"
        elif number == 8:
            text = "--- ---"
        elif number == 9:
            text = "---\u0398---"
        else:
            raise ValueError("Invalid number argument: {}".format(number))

        self.number = number
        self.setText(text)

    def getNumber(self):
        return self.number


class BoxButton(QPushButton):

    buttonNumberClicked = QtCore.pyqtSignal(int)

    def __init__(self, buttonNumber=0, parent=None):
        super().__init__(parent)


        self.buttonNumber = buttonNumber

        # Set the explicit size of the button and possibly text?.
        self.setMaximumWidth(25)
        self.clicked.connect(self._handleClicked)

    def _handleClicked(self):
        self.buttonNumberClicked.emit(self.buttonNumber)


