##############################################################################
# I Ching
##############################################################################

Author:  Ryan Luu
Email:   ryanluu@gmail.com

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

Dependencies to generate a .exe executable installer for MS Windows 
operating system:

  - MinGW
  - MSYS
  - cx_Freeze
  - NSIS
  - Subversion client

Dependencies to generate a .dmg install image for the Mac OS X 
operating system:

  - cx_Freeze
  - Subversion client


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

5) Change directory to the packaging folder and run the packaging script.

    [user@localhost ~]$ cd iching-read-only/packaging/
    [user@localhost packaging] ./package_for_windows

9) At the end of the above script output, the exact path to the created
installer executable is printed to the screen.  The path should be somewhere
within the 'dist' directory.


##############################################################################

Steps to generate an installable .dmg on Mac OS X operating system:

1) Follow steps 1 through 4 above to install dependencies.

2) Install cx_Freeze, which is used to convert the Python application
   to an binary executable.

    http://cx-freeze.sourceforge.net/

3) Check out project source code:

    svn checkout http://iching.googlecode.com/svn/trunk/ iching-read-only

4) Change directory to the top-level project directory.

    [user@localhost ~]$ cd iching-read-only

4a) Version 4.2.3 of cx_Freeze source code has a bug, so if you are
using this version and get the following error, read this step fully,
otherwise go to the next step.

Error in output is:

...
copying QtCore.framework/Versions/4/QtCore -> /Users/asdf/programming/qwer/dist/QtCore
Traceback (most recent call last):
File "/Library/Frameworks/Python.framework/Versions/3.1/bin/cxfreeze", line 5, in <module>
main()
File "/Library/Frameworks/Python.framework/Versions/3.1/lib/python3.1/site-packages/cx_Freeze/main.py", line 188, in main
freezer.Freeze()
File "/Library/Frameworks/Python.framework/Versions/3.1/lib/python3.1/site-packages/cx_Freeze/freezer.py", line 470, in Freeze
self._FreezeExecutable(executable)
File "/Library/Frameworks/Python.framework/Versions/3.1/lib/python3.1/site-packages/cx_Freeze/freezer.py", line 171, in _FreezeExecutable
exe.copyDependentFiles, scriptModule)
File "/Library/Frameworks/Python.framework/Versions/3.1/lib/python3.1/site-packages/cx_Freeze/freezer.py", line 455, in _WriteModules
self._CopyFile(module.file, target, copyDependentFiles)
File "/Library/Frameworks/Python.framework/Versions/3.1/lib/python3.1/site-packages/cx_Freeze/freezer.py", line 128, in _CopyFile
self._CopyFile(source, target, copyDependentFiles)
File "/Library/Frameworks/Python.framework/Versions/3.1/lib/python3.1/site-packages/cx_Freeze/freezer.py", line 120, in _CopyFile
shutil.copyfile(source, target)
File "/Library/Frameworks/Python.framework/Versions/3.1/lib/python3.1/shutil.py", line 66, in copyfile
fsrc = open(src, 'rb')
IOError: [Errno 2] No such file or directory: 'QtCore.framework/Versions/4/QtCore'


This error is due to cxfreeze assuming otool is returning an absolute
path in freezer.py, which is a false assumption.  This bug can be
fixed by modifying /Library/Frameworks/Python.framework/Versions/3.1/lib/python3.1/site-packages/cx_Freeze/freezer.py.  The modification is below.

sh-3.2# diff freezer.py freezer.py_orig 
252,253d251
<                     if not dependentFile.startswith("/"):
<                         dependentFile = "/Library/Frameworks/" + dependentFile


Bug filed is:
http://sourceforge.net/tracker/?func=detail&aid=3404531&group_id=84937&atid=574390

5) Change directory into the packaging directory and modify the
packaging script for Mac OS X, to have the correct version number and
release information.

    [user@localhost iching-read-only]$ cd packaging
    [user@localhost packaging]$ vim package_for_macosx.sh

6) Run the packaging script.  This will generate a .dmg archive for installing.

    [user@localhost packaging]$ ./package_for_macosx.sh

6) Change directory to the 'dist/MacOSX' directory to get the archive.

    [user@localhost packaging]$ cd ../dist/MacOSX/v*
    [user@localhost v1.0.5]$ ls
    iching-installer-mac-v1.0.5.dmg

##############################################################################

Directory contents:

iching
  |
  |- conf: Holds various configuration files such as the logging config.
  |
  |- dist: Holds the generated distributable package install files.
  |
  |- doc:  Holds this documentation.
  |
  |- packaging: 
  |        Holds scripts and configuration files for packaging to 
  |        distributable install files.
  | 
  |- resources: 
  |        Holds the I Ching texts, and image files.
  |
  |- src:  Holds the Python source code.
  |
  |- tps:  Holds third party software packages.

##############################################################################
