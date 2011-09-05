##############################################################################
# I Ching
##############################################################################

Author:  Ryan Luu
Email:   ryanluu@gmail.com
Version: 1.0.5
Release Date: 2011-09-05 02:01:28 -0400 (Mon, 05 Sep 2011)

##############################################################################

Description:

Application to quickly make I Ching castings.

##############################################################################

Requirements:

Dependencies to build/run this project are:

  - Python 3.1
  - Qt 4.6.3
  - SIP 4.11
  - PyQt 4.7.5

Dependencies to generate an installer .exe file on MS Windows operating system:

  - cx_Freeze
  - NSIS

##############################################################################

Steps to compile/run the software:

1) Install Python 3.1

    http://www.python.org/download/releases/3.1/

2) Install Qt 4.6.3

    ftp://ftp.trolltech.com/qt/source/

3) Install SIP 4.11

    Included in the svn source checkout.
    
    ./tps/pyqt/sip-4.11.tar.gz
    
4) Install PyQt 4.7.5

    Included in the svn source checkout.  Use the appropriate version
    for your operating system.

    ./tps/pyqt/PyQt-mac-gpl-4.7.5.tar.gz
    ./tps/pyqt/PyQt-win-gpl-4.7.5.zip
    ./tps/pyqt/PyQt-x11-gpl-4.7.5.tar.gz

5) Check out I Ching project source code:

    svn checkout http://iching.googlecode.com/svn/trunk/ iching-read-only

6) Change directory to the src directory.

    [user@localhost ~]$ cd iching-read-only/src/

7) Run the executable using Python.

    [user@localhost src]$ python3 ./main.py

##############################################################################

Steps to generate an installable .exe file on Microsoft Windows
operating systems:

1) Follow steps 1 through 4 above to install dependencies.

2) Install cx_Freeze, which is used to convert the Python application
   to an .exe executable.

    http://cx-freeze.sourceforge.net/

3) Install NSIS, which is used to generate the installer and uninstaller.

    http://nsis.sourceforge.net/Download

4) Check out project source code:

    svn checkout http://iching.googlecode.com/svn/trunk/ iching-read-only

5) Run cx_Freeze on main.py to generate the runnable .exe in the dist folder:

    [user@localhost ~]$ cd iching-read-only
    [user@localhost iching-read-only] /c/Python31/Scripts/cxfreeze src/main.py

6) Copy the Microsoft runtime libraries to the dist folder.

    [user@localhost iching-read-only] cp -r tps/microsoft/Microsoft.VC90.CRT/ dist/

7) Copy the NSIS script file from the conf directory to the top-level.

    [user@localhost iching-read-only]$ cp conf/windows_installer.nsi .

8) Run the NSIS.exe application and load the script 'windows_installer.nsi'.

9) The resulting installer executable will be generated and located in
   the top-level directory.


##############################################################################

Directory contents:

iching
  |
  |- conf: Holds the logging configuration and the NSIS installer 
  |        generator source file. 
  |
  |- doc:  Holds this documentation.
  |
  |- resources: Holds the I Ching texts, and icons.
  |
  |- src:  Holds the Python source code.
  |
  |- tps:  Holds third party software packages.

##############################################################################
