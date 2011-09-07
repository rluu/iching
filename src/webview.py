

from PyQt4.QtCore import *
from PyQt4.QtGui import *

# QtNetwork modules required for QtWebKit with cx_Freeze.
from PyQt4.QtNetwork import *

from PyQt4.QtWebKit import QWebPage
from PyQt4.QtWebKit import QWebView



class WebView(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.webView = QWebView()

        self.setModal(False)

        self.topButtonsToolbar = QToolBar()
        self.topButtonsToolbar.setMovable(False)
        self.topButtonsToolbar.\
            addAction(self.webView.pageAction(QWebPage.Back))
        self.topButtonsToolbar.\
            addAction(self.webView.pageAction(QWebPage.Forward))

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.topButtonsToolbar)
        self.layout.addWidget(self.webView)
        
        self.setLayout(self.layout)
        
    def load(self, url):
        """Loads the given URL into the QWebView.

        Arguments:
        url - QUrl object.
        """

        self.webView.load(url)

