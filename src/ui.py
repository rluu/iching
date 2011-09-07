
# For obtaining the line separator and directory separator.
import os

# For timestamp.
import datetime

# For logging.
import logging

import random

from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# For widgets used in the ui.
from widgets import *
from constants import *
from webview import *

from translations.alfred_huang import AlfredHuangTranslation
from translations.wilhelm_baynes import WilhelmBaynesTranslation
from translations.wu_wei import WuWeiTranslation
from translations.james_legge import JamesLeggeTranslation

import resources


class MainWindow(QMainWindow):
    """The QMainWindow class that is a multiple document interface (MDI)."""

    def __init__(self, 
                 appName, 
                 appVersion, 
                 appDate, 
                 appAuthor,
                 appAuthorEmail, 
                 parent=None):

        super().__init__(parent)

        self.log = logging.getLogger("ui.MainWindow")

        # Save off the application name, version and date.
        self.appName = appName
        self.appVersion = appVersion
        self.appDate = appDate
        self.appAuthor = appAuthor
        self.appAuthorEmail = appAuthorEmail
        self.appIcon = QIcon(":/images/rluu/appIcon.png")
        
        # Settings attributes that are set when _readSettings() is called.
        self.windowGeometry = QByteArray()
        self.windowState = QByteArray()
        self.splitterState = QByteArray()
    
        # Set application details so the we can use QSettings default
        # constructor later.
        QCoreApplication.setOrganizationName(appAuthor)
        QCoreApplication.setApplicationName(appName)

        # Initialize the random number generator.
        random.seed()

        # Used to keep track of what row we are on.
        self.currRow = 0

        # List of windows that hold QWebViews.
        self.webViews = []

        # Used to keep track of what button is what value.
        self.buttonToValue = []
        for i in range(16):
            self.buttonToValue.append(0)

        # Create widgets, etc.

        # Line to separate the toolbars and the widgets.
        self.hline1 = QFrame()
        self.hline1.setFrameShape(QFrame.HLine)

        lineEditWidthDefault = QTextEdit().sizeHint().width()

        self.timestampLabel = QLabel("Timestamp:")
        self.timestampValue = QLineEdit()
        self.timestampValue.setMinimumWidth(lineEditWidthDefault)
        self.timestampValue.setReadOnly(True)

        self.entryWidgetsLeftLayout = QHBoxLayout()
        self.entryWidgetsLeftLayout.addWidget(self.timestampLabel)
        self.entryWidgetsLeftLayout.addWidget(self.timestampValue)
        self.entryWidgetsLeftWidget = QWidget()
        self.entryWidgetsLeftWidget.setLayout(self.entryWidgetsLeftLayout)


        # Widgets to display the results.
        self.sumLabels = []
        for i in range(6):
            l = QLabel(" ")

            font = QFont("Courier New")
            l.setFont(font)

            self.sumLabels.append(l)

        self.sixMovableBars = []
        for i in range(6):
            l = BarLabel()
            self.sixMovableBars.append(l)

        self.firstStateBars = []
        for i in range(6):
            l = BarLabel()
            self.firstStateBars.append(l)

        self.secondStateBars = []
        for i in range(6):
            l = BarLabel()
            self.secondStateBars.append(l)

        font = QFont("Courier New", 14)
        font.setBold(True)

        nameLabelMinimumWidth = 148

        self.firstStateNumberLabel = QLabel()
        self.firstStateNumberLabel.setFont(font)
        self.firstStateNumberLabel.setAlignment(Qt.AlignHCenter)
        
        self.firstStateNameLabel = QLabel()
        self.firstStateNameLabel.setAlignment(Qt.AlignHCenter)
        self.firstStateNameLabel.setMinimumWidth(nameLabelMinimumWidth)

        self.firstStateNameWilhelmBaynesTranslationLabel = QLabel()
        self.firstStateNameWilhelmBaynesTranslationLabel.setAlignment(Qt.AlignHCenter)
        self.firstStateNameWilhelmBaynesTranslationLabel.setTextFormat(Qt.RichText)
        self.firstStateNameWilhelmBaynesTranslationLabel.setOpenExternalLinks(True)
        self.firstStateNameWilhelmBaynesTranslationLabel.setWordWrap(True)

        self.firstStateNameWuWeiTranslationLabel = QLabel()
        self.firstStateNameWuWeiTranslationLabel.setAlignment(Qt.AlignHCenter)
        self.firstStateNameWuWeiTranslationLabel.setTextFormat(Qt.RichText)
        self.firstStateNameWuWeiTranslationLabel.setOpenExternalLinks(True)
        self.firstStateNameWuWeiTranslationLabel.setWordWrap(True)

        self.firstStateNameAlfredHuangTranslationLabel = QLabel()
        self.firstStateNameAlfredHuangTranslationLabel.setAlignment(Qt.AlignHCenter)
        self.firstStateNameAlfredHuangTranslationLabel.setTextFormat(Qt.RichText)
        self.firstStateNameAlfredHuangTranslationLabel.setOpenExternalLinks(True)
        self.firstStateNameAlfredHuangTranslationLabel.setWordWrap(True)

        self.secondStateNumberLabel = QLabel()
        self.secondStateNumberLabel.setFont(font)
        self.secondStateNumberLabel.setAlignment(Qt.AlignHCenter)

        self.secondStateNameLabel = QLabel()
        self.secondStateNameLabel.setAlignment(Qt.AlignHCenter)
        self.secondStateNameLabel.setMinimumWidth(nameLabelMinimumWidth)

        self.secondStateNameWilhelmBaynesTranslationLabel = QLabel()
        self.secondStateNameWilhelmBaynesTranslationLabel.setAlignment(Qt.AlignHCenter)
        self.secondStateNameWilhelmBaynesTranslationLabel.setTextFormat(Qt.RichText)
        self.secondStateNameWilhelmBaynesTranslationLabel.setOpenExternalLinks(True)
        self.secondStateNameWilhelmBaynesTranslationLabel.setWordWrap(True)

        self.secondStateNameWuWeiTranslationLabel = QLabel()
        self.secondStateNameWuWeiTranslationLabel.setAlignment(Qt.AlignHCenter)
        self.secondStateNameWuWeiTranslationLabel.setTextFormat(Qt.RichText)
        self.secondStateNameWuWeiTranslationLabel.setOpenExternalLinks(True)
        self.secondStateNameWuWeiTranslationLabel.setWordWrap(True)

        self.secondStateNameAlfredHuangTranslationLabel = QLabel()
        self.secondStateNameAlfredHuangTranslationLabel.setAlignment(Qt.AlignHCenter)
        self.secondStateNameAlfredHuangTranslationLabel.setTextFormat(Qt.RichText)
        self.secondStateNameAlfredHuangTranslationLabel.setOpenExternalLinks(True)
        self.secondStateNameAlfredHuangTranslationLabel.setWordWrap(True)


        leftSideGridLayout = QGridLayout()
        numRows = 11


        col = 4
        leftSideGridLayout.\
            addWidget(self.firstStateNumberLabel, numRows - 5, col)
        leftSideGridLayout.\
            addWidget(self.firstStateNameLabel, numRows - 4, col)
        leftSideGridLayout.\
            addWidget(self.firstStateNameWilhelmBaynesTranslationLabel, numRows - 3, col)
        leftSideGridLayout.\
            addWidget(self.firstStateNameWuWeiTranslationLabel, numRows - 2, col)
        leftSideGridLayout.\
            addWidget(self.firstStateNameAlfredHuangTranslationLabel, numRows - 1, col)


        col = 6
        leftSideGridLayout.\
            addWidget(self.secondStateNumberLabel, numRows - 5, col)
        leftSideGridLayout.\
            addWidget(self.secondStateNameLabel, numRows - 4, col)
        leftSideGridLayout.\
            addWidget(self.secondStateNameWilhelmBaynesTranslationLabel, numRows - 3, col)
        leftSideGridLayout.\
            addWidget(self.secondStateNameWuWeiTranslationLabel, numRows - 2, col)
        leftSideGridLayout.\
            addWidget(self.secondStateNameAlfredHuangTranslationLabel, numRows - 1, col)

        i = 0
        for y in range(5, numRows):
            row = numRows - y - 1

            leftSideGridLayout.\
                addWidget(QLabel("   "), row, 0)

            leftSideGridLayout.\
                addWidget(self.sumLabels[i], row, 1)
                            
            leftSideGridLayout.\
                addWidget(self.sixMovableBars[i], row, 2)

            leftSideGridLayout.\
                addWidget(QLabel("        "), row, 3)

            leftSideGridLayout.\
                addWidget(self.firstStateBars[i], row, 4)

            leftSideGridLayout.\
                addWidget(QLabel("   "), row, 5)

            leftSideGridLayout.\
                addWidget(self.secondStateBars[i], row, 6)

            i += 1

        leftSideVLayout = QVBoxLayout()
        leftSideVLayout.addLayout(leftSideGridLayout)
        leftSideVLayout.addStretch()
        self.ichingResultsWidget = QWidget()
        self.ichingResultsWidget.setLayout(leftSideVLayout)
        
        self.boxButtons = []
        for i in range(16):
            button = BoxButton(i)
            self.boxButtons.append(button)

        rightSideGridLayout = QGridLayout()
        i = 0
        row = 0
        col = 0
        rightSideGridLayout.\
            addWidget(self.boxButtons[i], row, col)
        i += 1
        col += 1
        rightSideGridLayout.\
            addWidget(self.boxButtons[i], row, col)
        i += 1
        col += 1
        rightSideGridLayout.\
            addWidget(self.boxButtons[i], row, col)
        i += 1
        col += 1
        rightSideGridLayout.\
            addWidget(self.boxButtons[i], row, col)
        i += 1
        col += 1

        row += 1
        col = 0
        rightSideGridLayout.\
            addWidget(self.boxButtons[i], row, col)
        i += 1
        col += 1
        rightSideGridLayout.\
            addWidget(self.boxButtons[i], row, col)
        i += 1
        col += 1
        rightSideGridLayout.\
            addWidget(self.boxButtons[i], row, col)
        i += 1
        col += 1
        rightSideGridLayout.\
            addWidget(self.boxButtons[i], row, col)
        i += 1
        col += 1

        row += 1
        col = 0
        rightSideGridLayout.\
            addWidget(self.boxButtons[i], row, col)
        i += 1
        col += 1
        rightSideGridLayout.\
            addWidget(self.boxButtons[i], row, col)
        i += 1
        col += 1
        rightSideGridLayout.\
            addWidget(self.boxButtons[i], row, col)
        i += 1
        col += 1
        rightSideGridLayout.\
            addWidget(self.boxButtons[i], row, col)
        i += 1
        col += 1

        row += 1
        col = 0
        rightSideGridLayout.\
            addWidget(self.boxButtons[i], row, col)
        i += 1
        col += 1
        rightSideGridLayout.\
            addWidget(self.boxButtons[i], row, col)
        i += 1
        col += 1
        rightSideGridLayout.\
            addWidget(self.boxButtons[i], row, col)
        i += 1
        col += 1
        rightSideGridLayout.\
            addWidget(self.boxButtons[i], row, col)
        i += 1
        col += 1

        topSideLayout = QHBoxLayout()
        topSideLayout.addWidget(self.entryWidgetsLeftWidget)
        topSideLayout.addStretch()
        topSideWidget = QWidget()
        topSideWidget.setLayout(topSideLayout)

        rightSideLayout = QVBoxLayout()
        rightSideLayout.addLayout(rightSideGridLayout)
        rightSideLayout.addStretch()

        bottomAreaLayout = QHBoxLayout()
        bottomAreaLayout.addWidget(self.ichingResultsWidget)
        bottomAreaLayout.addSpacing(20)
        bottomAreaLayout.addLayout(rightSideLayout)
        bottomAreaWidget = QWidget()
        bottomAreaWidget.setLayout(bottomAreaLayout)

        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.addWidget(topSideWidget)
        self.splitter.addWidget(bottomAreaWidget)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.hline1)
        mainLayout.addWidget(self.splitter)

        self.mainWidget = QWidget()
        self.mainWidget.setLayout(mainLayout)

        self.setCentralWidget(self.mainWidget)

        # Create webviews used to display the various translations.

        # Wilhelm/Baynes Translation.
        self.webViewWilhelmBaynesTranslation = WebView(self)
        self.webViewWilhelmBaynesTranslation.hide()
        self.webViewWilhelmBaynesTranslation.\
            load(WilhelmBaynesTranslation.getUrl())
        self.webViewWilhelmBaynesTranslation.\
            setWindowTitle("Wilhelm/Baynes Translation")
        #self.webViewWilhelmBaynesTranslation.show()
        #self.webViewWilhelmBaynesTranslation.hide()

        # Wu Wei Translation.
        #self.webViewWuWeiTranslation = WebView(self)
        #self.webViewWuWeiTranslation.hide()
        #self.webViewWuWeiTranslation.\
        #    load(WuWeiTranslation.getUrl())
        #self.webViewWuWeiTranslation.\
        #    setWindowTitle("Wu Wei Translation")
        #self.webViewWuWeiTranslation.show()
        #self.webViewWuWeiTranslation.hide()

        # James Legge Translation.
        self.webViewJamesLeggeTranslation = WebView(self)
        self.webViewJamesLeggeTranslation.hide()
        self.webViewJamesLeggeTranslation.\
            load(JamesLeggeTranslation.getUrl())
        self.webViewJamesLeggeTranslation.\
            setWindowTitle("James Legge Translation")
        #self.webViewJamesLeggeTranslation.show()
        #self.webViewJamesLeggeTranslation.hide()

        
        # Create actions.
        self._createActions()

        # Create menus.
        self._createMenus()
        
        # Create the toolbars.
        self._createToolBars()

        # Connect signals and slots.
        for button in self.boxButtons:
            button.buttonNumberClicked.connect(self.boxClicked)

        # Simulate a click to clear everything.
        self._new()

        self._readSettings()

        self.restoreGeometry(self.windowGeometry)
        self.restoreState(self.windowState)
        self.splitter.restoreState(self.splitterState)

        self.setWindowTitle(self.appName)
        self.setWindowIcon(self.appIcon)

    def _createActions(self):
        """Creates the QAction objects that go into the Menu bar."""

        ####################
        # Create actions for the File menu.

        # Create the newIChingQueryAction.
        icon = QIcon(":/images/tango-icon-theme-0.8.90/32x32/actions/document-new.png")
        self.newAction = QAction(icon, "&New", self)
        self.newAction.setShortcut("Ctrl+n")
        self.newAction.setStatusTip("New I Ching Query")
        self.newAction.triggered.connect(self._new)

        # Create the printAction.
        icon = QIcon(":/images/tango-icon-theme-0.8.90/32x32/actions/document-print.png")
        self.printAction = QAction(icon, "&Print", self)
        self.printAction.setShortcut("Ctrl+p")
        self.printAction.setStatusTip("Print the Chart")
        self.printAction.triggered.connect(self._print)

        # Create the printPreviewAction.
        icon = QIcon(":/images/tango-icon-theme-0.8.90/32x32/actions/document-print-preview.png")
        self.printPreviewAction = QAction(icon, "Print Pre&view", self)
        self.printPreviewAction.\
            setStatusTip("Preview the document before printing")
        self.printPreviewAction.triggered.connect(self._printPreview)

        # Create the exitAppAction.
        icon = QIcon(":/images/tango-icon-theme-0.8.90/32x32/actions/system-log-out.png")
        self.exitAppAction = QAction(icon, "E&xit", self)
        self.exitAppAction.setShortcut("Ctrl+q")
        self.exitAppAction.setStatusTip("Exit the application")
        self.exitAppAction.triggered.connect(self._exitApp)


        ####################
        # Create actions for the References menu.

        icon = QIcon(":/images/rluu/book.png")
        self.wilhelmBaynesTranslationAction = \
            QAction(icon, "Wilhelm/Baynes Translation", self)
        self.wilhelmBaynesTranslationAction.\
            setStatusTip("Wilhelm/Baynes Translation")
        self.wilhelmBaynesTranslationAction.\
            triggered.connect(self._wilhelmBaynesTranslation)

        icon = QIcon(":/images/rluu/book.png")
        self.wuWeiTranslationAction = \
            QAction(icon, "Wu Wei Translation", self)
        self.wuWeiTranslationAction.\
            setStatusTip("Wu Wei Translation")
        self.wuWeiTranslationAction.\
            triggered.connect(self._wuWeiTranslation)

        icon = QIcon(":/images/rluu/book.png")
        self.jamesLeggeTranslationAction = \
            QAction(icon, "James Legge Translation", self)
        self.jamesLeggeTranslationAction.\
            setStatusTip("James Legge Translation")
        self.jamesLeggeTranslationAction.\
            triggered.connect(self._jamesLeggeTranslation)

        ####################
        # Create actions for the Help menu.

        icon = QIcon(":/images/tango-icon-theme-0.8.90/32x32/apps/help-browser.png")
        self.howToConsultIChingAction =  \
            QAction(icon, "How To Consult the I Ching", self)
        self.howToConsultIChingAction.\
            setStatusTip("How To Consult the I Ching")
        self.howToConsultIChingAction.triggered.connect(self._howToConsultIChing)
            
        icon = QIcon(":/images/rluu/iching.png")
        self.aboutIChingAction = QAction(icon, "About I Ching", self)
        self.aboutIChingAction.\
            setStatusTip("Show information about I Ching")
        self.aboutIChingAction.\
            triggered.connect(self._aboutIChing)

        self.aboutAction = QAction(self.appIcon, "&About This Application", self)
        self.aboutAction.\
            setStatusTip("Show information about this application")
        self.aboutAction.triggered.connect(self._about)

        self.aboutQtAction = \
            QAction(QIcon(":/images/qt/qt-logo.png"), "About &Qt", self)
        self.aboutQtAction.setStatusTip("Show information about Qt.")
        self.aboutQtAction.triggered.connect(self._aboutQt)


    def _createMenus(self):
        """Creates the menus in the menu bar."""

        # Create the File menu.
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.printAction)
        self.fileMenu.addAction(self.printPreviewAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAppAction)

        # Create the References menu.
        self.referenceMenu = self.menuBar().addMenu("&References")
        self.referenceMenu.addAction(self.wilhelmBaynesTranslationAction)
        self.referenceMenu.addAction(self.wuWeiTranslationAction)
        self.referenceMenu.addAction(self.jamesLeggeTranslationAction)

        # Create the Help menu.
        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.howToConsultIChingAction)
        self.helpMenu.addSeparator()
        self.helpMenu.addAction(self.aboutIChingAction)
        self.helpMenu.addSeparator()
        self.helpMenu.addAction(self.aboutAction)
        self.helpMenu.addAction(self.aboutQtAction)

    def _createToolBars(self):
        """Creates the toolbars with the QActions."""

        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.setObjectName("fileToolBar")
        self.fileToolBar.addAction(self.newAction)
        self.fileToolBar.addAction(self.printAction)
        self.fileToolBar.addAction(self.printPreviewAction)

        self.referencesToolBar = self.addToolBar("References")
        self.referencesToolBar.setObjectName("referencesToolBar")
        self.referencesToolBar.addAction(self.wilhelmBaynesTranslationAction)
        self.referencesToolBar.addAction(self.wuWeiTranslationAction)
        self.referencesToolBar.addAction(self.jamesLeggeTranslationAction)

        self.helpToolBar = self.addToolBar("Help")
        self.helpToolBar.setObjectName("helpToolBar")
        self.helpToolBar.addAction(self.howToConsultIChingAction)
        self.helpToolBar.addAction(self.aboutIChingAction)
        self.helpToolBar.addAction(self.aboutAction)
        self.helpToolBar.addAction(self.aboutQtAction)

    def _writeSettings(self):
        """
        Writes current settings values to the QSettings object.

        This function uses QSettings and assumes that the calls to
        QCoreApplication.setOrganizationName(), and 
        QCoreApplication.setApplicationName() have been called 
        previously (so that the QSettings constructor can be called 
        without any parameters specified).
        """

        self.log.debug("Writing settings...")

        # Preference settings.
        settings = QSettings() 

        # Window geometry.
        key = "ui/MainWindow/windowGeometry"
        settings.setValue(key, self.saveGeometry())

        # Window state.
        key = "ui/MainWindow/windowState"
        settings.setValue(key, self.saveState())

        # Splitter state.
        key = "ui/MainWindow/splitter"
        settings.setValue(key, self.splitter.saveState())


        self.log.debug("Done writing settings...")

    def _readSettings(self):
        """
        Reads in QSettings values for preferences and default values.

        This function uses QSettings and assumes that the calls to
        QCoreApplication.setOrganizationName(), and 
        QCoreApplication.setApplicationName() have been called 
        previously (so that the QSettings constructor can be called 
        without any parameters specified).
        """

        self.log.debug("Reading settings...")

        # Preference settings.
        settings = QSettings() 

        # Window geometry.
        self.windowGeometry = \
            settings.value("ui/MainWindow/windowGeometry")
        if self.windowGeometry == None:
            self.windowGeometry = QByteArray()
            
        # Window state.
        self.windowState = \
            settings.value("ui/MainWindow/windowState")
        if self.windowState == None:
            self.windowState = QByteArray()

        # Splitter state.
        self.splitterState = \
            settings.value("ui/MainWindow/splitter")
        if self.splitterState == None:
            self.splitterState = QByteArray()

        self.log.debug("Done reading settings...")

    def randomizeButtonToValue(self):

        # Odds of a 6 is 1 in 16.
        # Odds of a 7 is 5 in 16.
        # Odds of a 8 is 7 in 16.
        # Odds of a 9 is 3 in 16.
        marbles = []
        marbles.append(6)
        marbles.append(7)
        marbles.append(7)
        marbles.append(7)
        marbles.append(7)
        marbles.append(7)
        marbles.append(8)
        marbles.append(8)
        marbles.append(8)
        marbles.append(8)
        marbles.append(8)
        marbles.append(8)
        marbles.append(8)
        marbles.append(9)
        marbles.append(9)
        marbles.append(9)

        i = 0
        while len(marbles) > 0:
            marbleIndex = random.randrange(0, len(marbles))
            marbleValue = marbles[marbleIndex]
            marbles.remove(marbleValue)
            self.buttonToValue[i] = marbleValue
            i += 1
        
        self.log.debug("New randomized array is: " + os.linesep + \
                       "{}".format(self.buttonToValue))



    def boxClicked(self, number):
        """Run when a box is clicked that is simulating yarrow sticks."""

        self.log.debug("box clicked is index: {}".format(number))
        value = self.buttonToValue[number]
        self.log.debug("value for that index is: {}".format(value))

        self.sumLabels[self.currRow].setText(str(value))
        self.sixMovableBars[self.currRow].drawLineAsNum(value)

        if value == 6:
            self.firstStateBars[self.currRow].drawLineAsNum(8)
            self.secondStateBars[self.currRow].drawLineAsNum(7)
        elif value == 7:
            self.firstStateBars[self.currRow].drawLineAsNum(7)
            self.secondStateBars[self.currRow].drawLineAsNum(7)
        elif value == 8:
            self.firstStateBars[self.currRow].drawLineAsNum(8)
            self.secondStateBars[self.currRow].drawLineAsNum(8)
        elif value == 9:
            self.firstStateBars[self.currRow].drawLineAsNum(7)
            self.secondStateBars[self.currRow].drawLineAsNum(8)
        else:
            self.log.error("Invalid value!")

        self.currRow += 1

        if self.currRow == 6:
            # We have finished our six lines.
            self.currRow = 0
            self.updateHexagramLabels()

            self.setBoxButtonsEnabled(False)
            self.printAction.setEnabled(True)
            self.printPreviewAction.setEnabled(True)

        self.randomizeButtonToValue()

    def updateHexagramLabels(self):

        endl = "<br />"

        lines = \
            "{}{}{}{}{}{}".\
            format(self.firstStateBars[0].getNumber(),
                   self.firstStateBars[1].getNumber(),
                   self.firstStateBars[2].getNumber(),
                   self.firstStateBars[3].getNumber(),
                   self.firstStateBars[4].getNumber(),
                   self.firstStateBars[5].getNumber())
        
        self.log.debug("First State: lines is: {}".format(lines))
        
        kuaNumber = IChingConstants.linesToKuaNumber[lines]
        self.log.debug("First State: kuaNumber is: {}".format(kuaNumber))
        
        kuaName = IChingConstants.kuaNumberToKuaName[kuaNumber]
        self.log.debug("First State: kuaName is: {}".format(kuaName))
        
        kuaNameTranslatedWilhelmBaynes = \
            WilhelmBaynesTranslation.kuaNumberToKuaTranslation[kuaNumber]

        kuaNameTranslatedWuWei = \
            WuWeiTranslation.kuaNumberToKuaTranslation[kuaNumber]

        kuaNameTranslatedAlfredHuang = \
            AlfredHuangTranslation.kuaNumberToKuaTranslation[kuaNumber]

        self.firstStateNumberLabel.setText(str(kuaNumber))
        self.firstStateNameLabel.setText(kuaName)
        self.firstStateNameWilhelmBaynesTranslationLabel.\
            setText(kuaNameTranslatedWilhelmBaynes)
        self.firstStateNameWilhelmBaynesTranslationLabel.setFrameStyle(QFrame.Box)
        self.firstStateNameWuWeiTranslationLabel.\
            setText(kuaNameTranslatedWuWei)
        self.firstStateNameWuWeiTranslationLabel.setFrameStyle(QFrame.Box)
        self.firstStateNameAlfredHuangTranslationLabel.\
            setText(kuaNameTranslatedAlfredHuang)
        self.firstStateNameAlfredHuangTranslationLabel.setFrameStyle(QFrame.Box)

        lines = \
            "{}{}{}{}{}{}".\
            format(self.secondStateBars[0].getNumber(),
                   self.secondStateBars[1].getNumber(),
                   self.secondStateBars[2].getNumber(),
                   self.secondStateBars[3].getNumber(),
                   self.secondStateBars[4].getNumber(),
                   self.secondStateBars[5].getNumber())
        
        self.log.debug("Second State: lines is: {}".format(lines))
        
        kuaNumber = IChingConstants.linesToKuaNumber[lines]
        self.log.debug("Second State: kuaNumber is: {}".format(kuaNumber))
        
        kuaName = IChingConstants.kuaNumberToKuaName[kuaNumber]
        self.log.debug("Second State: kuaName is: {}".format(kuaName))
        
        kuaNameTranslatedWilhelmBaynes = \
            WilhelmBaynesTranslation.kuaNumberToKuaTranslation[kuaNumber]

        kuaNameTranslatedWuWei = \
            WuWeiTranslation.kuaNumberToKuaTranslation[kuaNumber]

        kuaNameTranslatedAlfredHuang = \
            AlfredHuangTranslation.kuaNumberToKuaTranslation[kuaNumber]

        self.secondStateNumberLabel.setText(str(kuaNumber))
        self.secondStateNameLabel.setText(kuaName)
        self.secondStateNameWilhelmBaynesTranslationLabel.\
            setText(kuaNameTranslatedWilhelmBaynes)
        self.secondStateNameWilhelmBaynesTranslationLabel.setFrameStyle(QFrame.Box)
        self.secondStateNameWuWeiTranslationLabel.\
            setText(kuaNameTranslatedWuWei)
        self.secondStateNameWuWeiTranslationLabel.setFrameStyle(QFrame.Box)
        self.secondStateNameAlfredHuangTranslationLabel.\
            setText(kuaNameTranslatedAlfredHuang)
        self.secondStateNameAlfredHuangTranslationLabel.setFrameStyle(QFrame.Box)


    def setBoxButtonsEnabled(self, enabled=True):
        """This function enables or disables the box buttons that are used
        for casting in I Ching.  If the buttons are enabled then they are
        also visible.  If they are disabled then the buttons are set as
        hidden."""

        for button in self.boxButtons:
            button.setEnabled(enabled)
    
    def closeEvent(self, closeEvent):
        """Attempts to close the QMainWindow.  Does any cleanup necessary."""
        self._writeSettings()
        closeEvent.accept()

    def _new(self):
        """Resets all the fields for making a new I Ching Query."""

        # Clear all widgets and reset counters.
        for label in self.sumLabels:
            label.setText(" ")

        for label in self.sixMovableBars:
            label.clear()

        for label in self.firstStateBars:
            label.clear()

        for label in self.secondStateBars:
            label.clear()

        self.firstStateNumberLabel.clear()
        self.firstStateNameLabel.clear()
        self.firstStateNameWilhelmBaynesTranslationLabel.clear()
        self.firstStateNameWilhelmBaynesTranslationLabel.setFrameStyle(QFrame.NoFrame)
        self.firstStateNameWuWeiTranslationLabel.clear()
        self.firstStateNameWuWeiTranslationLabel.setFrameStyle(QFrame.NoFrame)
        self.firstStateNameAlfredHuangTranslationLabel.clear()
        self.firstStateNameAlfredHuangTranslationLabel.setFrameStyle(QFrame.NoFrame)

        self.secondStateNumberLabel.clear()
        self.secondStateNameLabel.clear()
        self.secondStateNameWilhelmBaynesTranslationLabel.clear()
        self.secondStateNameWilhelmBaynesTranslationLabel.setFrameStyle(QFrame.NoFrame)
        self.secondStateNameWuWeiTranslationLabel.clear()
        self.secondStateNameWuWeiTranslationLabel.setFrameStyle(QFrame.NoFrame)
        self.secondStateNameAlfredHuangTranslationLabel.clear()
        self.secondStateNameAlfredHuangTranslationLabel.setFrameStyle(QFrame.NoFrame)

        self.currRow = 0

        now = datetime.datetime.now()
        timestampFmt = "%Y-%m-%d %H:%M:%S %Z %z"
        timestampStr = "{}".format(now.strftime(timestampFmt))
        self.timestampValue.setText(timestampStr)

        self.randomizeButtonToValue()

        self.setBoxButtonsEnabled(True)
        self.printAction.setEnabled(False)
        self.printPreviewAction.setEnabled(False)


    def _print(self):
        """Brings up a dialog to confirm printing."""

        printer = QPrinter(QPrinter.HighResolution)
        printDialog = QPrintDialog(printer)
        
        rv = printDialog.exec_()
            
        if rv == QDialog.Accepted:
            self._printToPrinter(printer)


    def _printPreview(self):
        """Does a previews of what would be printed if print is called."""

        printPreviewDialog = QPrintPreviewDialog()

        printPreviewDialog.paintRequested.connect(self._printToPrinter)

        printPreviewDialog.exec()

    def _printToPrinter(self, printer):
        """Actually does the printing to the given printer."""

        if printer.isValid() == False:
            title = "Error"
            errMsg = "Aborting print job.  " + \
                "The current printer configuration is invalid."

            QMessageBox.warning(self, title, errMsg)
            return
            
        # Print.

        # Get page size info so that we can do QPixmap scaling.
        pageRect = printer.pageRect()
        self.log.debug("page rect: t={}, l={}, b={}, r={}, w={}, h={}".\
            format(pageRect.top(),
                   pageRect.left(),
                   pageRect.bottom(),
                   pageRect.right(),
                   pageRect.width(),
                   pageRect.height()))

        # Get a pixmap of the self.entryWidgetsLeftWidget
        pixmapTop = QPixmap.grabWidget(self.entryWidgetsLeftWidget)
        newSize = QSize(pageRect.width() * (3/4), \
                        pageRect.height() * (1/3))
        pixmapTop = pixmapTop.scaled(newSize, 
                                     Qt.KeepAspectRatio,
                                     Qt.SmoothTransformation)

        # Get a pixmap of the self.ichingResultsWidget.
        pixmapMid = QPixmap.grabWidget(self.ichingResultsWidget)
        newSize = QSize(pageRect.width() * (3/4), \
                        pageRect.height() * (1/3))
        pixmapMid = pixmapMid.scaled(newSize, 
                                     Qt.KeepAspectRatio,
                                     Qt.SmoothTransformation)

        self.log.debug("printing...")
        painter = QPainter()
        painter.begin(printer)
        painter.drawPixmap(pageRect.left(), 
                           pageRect.top(), 
                           pixmapTop)
        painter.drawPixmap(pageRect.left(), 
                           pageRect.top() + pixmapTop.rect().height(), 
                           pixmapMid)
        painter.end()

    def _exitApp(self):
        qApp.closeAllWindows()


    def _wilhelmBaynesTranslation(self):
        """Displays the Wilhelm/Baynes translation of the I Ching."""

        self.webViewWilhelmBaynesTranslation.show()
        #webview = WebView(self)
        #webview.load(WilhelmBaynesTranslation.getUrl())
        #webview.setWindowTitle("Wilhelm/Baynes Translation")
        #webview.show()

    def _wuWeiTranslation(self):
        """Displays the Wu Wei translation of the I Ching."""

        title = "Wu Wei Translation"
        message = "Wu Wei translation is not currently supported."
        
        QMessageBox.about(self, title, message)

        # TODO:  In the future, add the Wu Wei translation.
        

    def _jamesLeggeTranslation(self):
        """Displays the James Legge translation of the I Ching."""

        self.webViewJamesLeggeTranslation.show()
        #webview = WebView(self)
        #webview.load(JamesLeggeTranslation.getUrl())
        #webview.setWindowTitle("James Legge Translation")
        #webview.show()

    def _howToConsultIChing(self):
        """Opens up a dialog with information on how to consult the I Ching."""

        endl = os.linesep
        
        title = "How To Consult I Ching"
        message = "This feature has not been developed yet.  " + endl + \
                  "Please check back later!"
        
        QMessageBox.about(self, title, message)
        
        # TODO:  Add some code for the help.

    def _aboutIChing(self):
        """Opens up a popup window displaying information about I Ching."""

        endl = os.linesep
        
        title = "How To Consult I Ching"
        message = "This feature has not been developed yet.  " + endl + \
                  "Please check back later!"
        
        QMessageBox.about(self, title, message)
        
        # TODO:  Add some code for the I Ching about.

    def _about(self):
        """Opens a popup window displaying information about this
        application.
        """

        endl = os.linesep

        title = "About"

        message = self.appName + endl + \
                  endl + \
                  "This is a PyQt application that " + \
                  "simulates casting yarrow sticks for I Ching." + \
                  endl + \
                  "Simply click on the box buttons randomly until " + \
                  "the casting is complete.  " + \
                  endl + \
                  "Then read the I Ching text associated with the " + \
                  "hexagram numbers obtained from the casting." + \
                  endl + \
                  endl + \
                  "Version: " + self.appVersion + endl + \
                  "Released: " + self.appDate + endl + \
                  endl + \
                  "Author: " + self.appAuthor + endl + \
                  "Email: " + self.appAuthorEmail

        QMessageBox.about(self, title, message)

    def _aboutQt(self):
        """Opens a popup window displaying information about the Qt
        toolkit used in this application.
        """

        title = "About Qt"
        QMessageBox.aboutQt(self, title)


