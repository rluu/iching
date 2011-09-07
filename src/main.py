#!/usr/bin/env python3

# For obtaining current directory path information, and creating directories
import os
import sys
    
# For parsing command-line options
from optparse import OptionParser  

# For logging.
import logging
import logging.handlers
import logging.config

# Import PyQt classes.
from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Import from this project.
from ui import MainWindow

##############################################################################

__version__ = "1.0.6"
__date__ = "Wed Sep  7 07:45:41 EDT 2011"


# Application Name
APP_NAME = "I Ching"

# Application Version obtained from subversion revision.
APP_VERSION = __version__

# Application Date obtain from last subversion commit date.
APP_DATE = __date__

# Directory where log files will be written.
#LOG_DIR = os.path.join(sys.path[0], "logs")
LOG_DIR = os.path.join(sys.path[0],
                       ".." + os.sep + "logs")

# Location of the config file for logging.
LOG_CONFIG_FILE = os.path.join(sys.path[0],
                               ".." + os.sep + "conf" + os.sep + "logging.conf")

# Application author
APP_AUTHOR = "Ryan Luu"

# Application author's email address.
APP_AUTHOR_EMAIL = "ryanluu@gmail.com"

##############################################################################

def main():
    # Parse command-line arguments.
    (options, args) = parseCommandlineArgs()
    
    # Set up the logger.

    # Parsing the log config file doesn't work on the current version
    # of cx_Freeze (on Windows and on Mac).  The author of cx_Freeze
    # knows about this bug and hopefully the next release of cx_Freeze
    # addresses this issue.  Until then, only parse the config file if
    # this file is referenced as a .py file.
    if sys.argv[0].split(".")[-1] == "py":
        logging.config.fileConfig(LOG_CONFIG_FILE)
    log = logging.getLogger("main")

    log.info("##########################################");
    log.info("# Starting " + sys.argv[0] + ", version " + APP_VERSION);
    log.info("##########################################");

    # Create the Qt application.
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setWindowIcon(QIcon(":/images/rluu/appIcon.png"))

    # Create the main window for the app and show it.
    mainWindow = MainWindow(APP_NAME, 
                            APP_VERSION, 
                            APP_DATE, 
                            APP_AUTHOR, 
                            APP_AUTHOR_EMAIL)
    mainWindow.show()

    # Cleanup and close the application when the last window is closed.
    app.lastWindowClosed.connect(logging.shutdown)
    app.lastWindowClosed.connect(app.quit)

    return app.exec_()


def parseCommandlineArgs():
    """Parses the arguments specified on the command-line.
    Returns (options, args) for the options and arguments passed"""

    # Create the parser
    parser = OptionParser()

    # Specify all valid options.
    parser.add_option("-v", "--version",
                      action="store_true",
                      dest="version",
                      default=False,
                      help="Display application version info and author " + \
                      "contact.")
    
    # Parse the arguments into options.
    global options
    (options, args) = parser.parse_args()

    # Print version information if the flag was used.
    if (options.version == True):
        print(APP_NAME + " (Version " + APP_VERSION + ")")
        print("By " + APP_AUTHOR + ", " + APP_AUTHOR_EMAIL)
        sys.exit(0)

    return (options, args)



##############################################################################

if __name__=="__main__":
    exitCode = main()
    sys.exit(exitCode)

##############################################################################


