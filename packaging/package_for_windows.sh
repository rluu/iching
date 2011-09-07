#!/bin/sh
##############################################################################
# 
# File: package_for_windows.sh
# 
# Description:
#
#   Script for packaging the application into a setup .exe executable
#   to be run on Microsoft Windows.
#
#   After running this script, the resulting executable will be placed in:
#
#        ../dist/Windows/$APP_VERSION/iching-installer-win32-$APP_VERSION.exe
#
# Dependencies:
#   MinGW
#   MSYS
#   cx_Freeze
#   NSIS
#   Subversion client
#
# Usage:
# 
#   ./package_for_windows.sh
#
##############################################################################

##############################################################################
# Global Variables
##############################################################################

# Directory where this script lives, relative to the current working directory.
DIR=`dirname $0`

APP_NAME="I Ching"

APP_VERSION_PREFIX="v"

# This obtains the application version number from the global Python
# variable defined in main.py.
APP_VERSION_NUMBER=`grep "__version__"  $DIR/../src/main.py | grep -v "APP_VERSION" | cut -d'"' -f 2`

APP_VERSION="${APP_VERSION_PREFIX}${APP_VERSION_NUMBER}"

# Obtains the build number, which is the subversion revision of the
# top-level directory.
APP_BUILD_NUMBER=`svnversion $DIR/.. | cut -d':' -f2`

# Operating system.  
OPERATING_SYSTEM=Windows

# Distribution directory.
DISTRIB_DIRNAME=dist

# cx_Freeze executable.
CXFREEZE=cxfreeze

# 
# Name of the Python script to pass to cx_Freeze.
APP_MAIN_SCRIPT=src/main.py

# Microsoft runtime library directory.
MS_RUNTIME_DIR=tps/microsoft/Microsoft.VC90.CRT

# NSIS template input file.
NSIS_SCRIPTNAME=windows_installer.nsi
NSIS_TEMPLATE_SCRIPTNAME=windows_installer.nsi.in
NSIS_TEMPLATE_SCRIPT="packaging/$OPERATING_SYSTEM/$NSIS_TEMPLATE_SCRIPTNAME"

# Path to the icon to use in the application package.
APP_MAIN_ICONNAME=appIcon.ico
APP_MAIN_ICON="resources\\images\\rluu\\$APP_MAIN_ICONNAME"

APP_INSTALL_PACKAGE_NAME="iching-installer-win32-${APP_VERSION}-${APP_BUILD_NUMBER}.exe"

##############################################################################

echo "########################################################################"
echo "Creating Windows installer for ${APP_NAME} ${APP_VERSION}-${APP_BUILD_NUMBER}"
echo "`date`"
echo "########################################################################"

# Go to the top-level directory.
# This script assumes that we're in the 'packaging' subdirectory of the
# project, so this will just go to one directory above that.
cd $DIR/../

# Destination directory to deploy to.
DEST_DIR="${DISTRIB_DIRNAME}/${OPERATING_SYSTEM}/${APP_VERSION}-${APP_BUILD_NUMBER}"

# If directory exists, remove and recreate it.
if [ -d "$DEST_DIR" ]; then
    echo "Destination directory $DEST_DIR exists.  Removing before recreating."
    rm -rf "$DEST_DIR"
fi

# Make a directory to place the distribution in.
mkdir -p "$DEST_DIR"

# Make a directory to place the cx_Freeze output.
CXFREEZE_INSTALL_DIR="$DEST_DIR/dist"
mkdir -p "$CXFREEZE_INSTALL_DIR"

# Run cx_Freeze to gather all the dependencies in the dist directory.
echo "Running cxfreeze ..."
$CXFREEZE --target-dir="$CXFREEZE_INSTALL_DIR" "$APP_MAIN_SCRIPT"

# Copy over the Microsoft runtime libraries.
echo "Copying the required Microsoft runtime libraries ..."
cp -r "$MS_RUNTIME_DIR" "$CXFREEZE_INSTALL_DIR"

# Copy some of the directories.
SUBDIRS="conf doc logs resources"
for d in $SUBDIRS; do

    echo "Copying $d ..."

    # Create the subdirectory.
    mkdir -p "$DEST_DIR/$d"

    # Copy the subdirectory contents if the source directory $d is not empty.
    if [ `find $d | wc -l` -gt 1 ]; then
        #echo "Directory $d is not empty."
        for f in `ls $d`; do
            cmd="cp -r $d/$f $COPY_DEST_DIR/$d/"
            #echo "Running command $cmd"
            $cmd
        done
    fi

    # Remove the ".svn" hidden directories.
    find $DEST_DIR/$d -name "\.svn" | xargs rm -rf

    # Remove any extra files that aren't needed.
    find $DEST_DIR/$d -name "*.log" | xargs rm -rf
    find $DEST_DIR/$d -name "*.pyc" | xargs rm -rf
    find $DEST_DIR/$d -name "Makefile*" | xargs rm -rf
    find $DEST_DIR/$d -name "16x16" | xargs rm -rf
    find $DEST_DIR/$d -name "22x22" | xargs rm -rf
    find $DEST_DIR/$d -name "scalable" | xargs rm -rf

    # For now, remove pdfs, since they are big.  We may want to
    # include them in the future.
    find $DEST_DIR/$d -name "*.pdf" | xargs rm -rf
done


# Copy the icon.
echo "Copying app icon ..."
cp $APP_MAIN_ICON $APP_PACKAGE_DIR/Contents/Resources/

# Copy the NSIS configuration script.
echo "Copying template NSIS file ..."
cp "$NSIS_TEMPLATE_SCRIPT" "$CXFREEZE_INSTALL_DIR/$NSIS_SCRIPTNAME"
NSIS_SCRIPT="$CXFREEZE_INSTALL_DIR/$NSIS_SCRIPTNAME"

# Do some sed replaces to put actual values in the NSIS script file.
echo "Doing sed replaces to the $NSIS_SCRIPT file ..."
sed -i -e "s/APP_NAME/${APP_NAME}/g" $NSIS_SCRIPT
sed -i -e "s/APP_MAIN_ICON/${APP_MAIN_ICON}/g" $NSIS_SCRIPT
sed -i -e "s/APP_INSTALL_PACKAGE_NAME/${APP_INSTALL_PACKAGE_NAME}/g" $NSIS_SCRIPT

# Remove temporary file created by the above sed commands.
for f in `ls ${NSIS_SCRIPT}*`; do
    if [ "$f" != "${APP_INFO_PLIST}" ]; then
        echo "Removing temp generated sed file ..."
        rm $f
    fi
done
 
# Do some cleanup
echo "Doing post-cleanup..."

echo "Removing working app package directory..."
rm -rf "$APP_PACKAGE_DIR"

echo "Removing cx_Freeze working directory..."
rm -rf "$CXFREEZE_INSTALL_DIR"

echo "Clean-up complete."
echo ""
echo "Installer archive is now created at location: "
echo "`pwd`/$APP_INSTALL_PACKAGE"

#echo "Done."
exit 0 
