#!/bin/sh
##############################################################################
# 
# File: package_for_macosx.sh
# 
# Description:
#
#   Script for packaging to a Mac OS X application and into an install
#   .dmg package.  The resulting package gets placed in a file such as:
#
#        ../dist/MacOSX/$APP_VERSION/iching-installer-mac-$APP_VERSION.dmg
#
# Dependencies:
#   cx_Freeze
#   
# Usage:
# 
#   ./package_for_macosx.sh
#
##############################################################################

##############################################################################
# Global Variables
##############################################################################

# Directory where this script lives, relative to the current working directory.
DIR=`dirname $0`

# Go to the top-level directory.
# This script assumes that it exists in the 'packaging' subdirectory of the
# project, so this will just go to one directory above that.
cd $DIR/../
TOPLEVEL_DIR="`pwd`"

APP_NAME="I Ching"
APP_NAME_NOSPACES="IChing"

# For some reason, the bundle name needs to be without spaces or else
# it doesn't launch in Mac OS X.
APP_BUNDLE_NAME="IChing.app"

APP_VERSION_PREFIX="v"

# This obtains the application version number from the global Python
# variable defined in main.py.
APP_VERSION_NUMBER=`grep "__version__"  "$TOPLEVEL_DIR/src/main.py" | grep -v "APP_VERSION" | cut -d'"' -f 2`

APP_VERSION="${APP_VERSION_PREFIX}${APP_VERSION_NUMBER}"

# Obtains the build number, which is the subversion revision of the
# top-level directory.
APP_BUILD_NUMBER=`svnversion "$TOPLEVEL_DIR" | cut -d':' -f2`

# Operating system.  
OPERATING_SYSTEM=MacOSX

# Distribution directory.
DISTRIB_DIRNAME=dist

# cx_Freeze executable.
CXFREEZE=cxfreeze

# Name of the Python script to pass to cx_Freeze.
APP_MAIN_SCRIPT=src/main.py

# Path to the icon to use in the application package.
APP_MAIN_ICONNAME=appIcon.icns
APP_MAIN_ICON=resources/images/rluu/$APP_MAIN_ICONNAME

APP_LAUNCH_SCRIPTNAME=iching.sh
APP_LAUNCH_SCRIPT=packaging/$OPERATING_SYSTEM/$APP_LAUNCH_SCRIPTNAME
APP_INFO_PLISTNAME=Info.plist
APP_TEMPLATE_INFO_PLISTNAME=Info.plist.in
APP_TEMPLATE_INFO_PLIST=packaging/$OPERATING_SYSTEM/$APP_TEMPLATE_INFO_PLISTNAME

APP_BUNDLE_IDENTIFIER="com.ryanluu.iching"
APP_BUNDLE_UNIQUE_SIGNATURE="qsoo"

# Image used in the background of the installer .dmg image.
DMG_BACKGROUND_IMGNAME=iching_dmg_background.png
DMG_BACKGROUND_IMG=resources/images/rluu/$DMG_BACKGROUND_IMGNAME

APP_INSTALL_PACKAGE_NAME="iching-installer-mac-${APP_VERSION}-${APP_BUILD_NUMBER}.dmg"

##############################################################################

echo "########################################################################"
echo "Creating Mac OS X .dmg package for ${APP_NAME} ${APP_VERSION}-${APP_BUILD_NUMBER}"
echo "`date`"
echo "########################################################################"

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
CXFREEZE_INSTALL_DIR="$DEST_DIR/cxfreeze_output"
mkdir -p "$CXFREEZE_INSTALL_DIR"

# Run cx_Freeze to gather all the dependencies in the dist directory.
echo "Running cxfreeze ..."
$CXFREEZE --target-dir="$CXFREEZE_INSTALL_DIR" "$APP_MAIN_SCRIPT"

# Make the app directory and it's structure.
echo "Making app bundle ..."
APP_PACKAGE_DIRNAME="$APP_BUNDLE_NAME"
echo "APP_PACKAGE_DIRNAME=$APP_PACKAGE_DIRNAME"
APP_PACKAGE_DIR="$DEST_DIR/$APP_PACKAGE_DIRNAME"
echo "APP_PACKAGE_DIR=$APP_PACKAGE_DIR"
mkdir -p "$APP_PACKAGE_DIR"
mkdir -p "$APP_PACKAGE_DIR/Contents"
mkdir -p "$APP_PACKAGE_DIR/Contents/MacOS"
mkdir -p "$APP_PACKAGE_DIR/Contents/Resources"

# Copy the cx_Freeze output.
echo "Copying cxfreeze files to the app bundle ..."
mkdir -p "$APP_PACKAGE_DIR/Contents/MacOS/dist"
cp -r $CXFREEZE_INSTALL_DIR/* $APP_PACKAGE_DIR/Contents/MacOS/dist

# Copy some of the directories.
COPY_DEST_DIR="$APP_PACKAGE_DIR/Contents/MacOS"
SUBDIRS="conf doc logs resources"
for d in $SUBDIRS; do

    echo "Copying $d ..."

    # Create the subdirectory.
    mkdir -p "$COPY_DEST_DIR/$d"

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
    find $COPY_DEST_DIR/$d -name "\.svn" | xargs rm -rf

    # Remove any extra files that aren't needed.
    find $COPY_DEST_DIR/$d -name "*.log" | xargs rm -rf
    find $COPY_DEST_DIR/$d -name "*.pyc" | xargs rm -rf
    find $COPY_DEST_DIR/$d -name "Makefile*" | xargs rm -rf
    find $COPY_DEST_DIR/$d -name "16x16" | xargs rm -rf
    find $COPY_DEST_DIR/$d -name "22x22" | xargs rm -rf
    find $COPY_DEST_DIR/$d -name "scalable" | xargs rm -rf

    # For now, remove pdfs, since they are big.  We may want to
    # include them in the future.
    find $COPY_DEST_DIR/$d -name "*.pdf" | xargs rm -rf
done

# Copy the launch script.
echo "Copying launch script to the app bundle ..."
cp $APP_LAUNCH_SCRIPT $APP_PACKAGE_DIR/Contents/MacOS/
chmod +x "$APP_PACKAGE_DIR/Contents/MacOS/$APP_LAUNCH_SCRIPTNAME"

# Copy the icon.
echo "Copying app icon to the app bundle ..."
cp $APP_MAIN_ICON $APP_PACKAGE_DIR/Contents/Resources/

# Copy the template Info.plist file.
echo "Copying template Info.plist file to the app bundle ..."
cp $APP_TEMPLATE_INFO_PLIST $APP_PACKAGE_DIR/Contents/$APP_INFO_PLISTNAME
APP_INFO_PLIST="$APP_PACKAGE_DIR/Contents/$APP_INFO_PLISTNAME"

# Do some sed replaces to put actual values in the Info.plist file.
echo "Doing sed replaces to the Info.plist file ..."
sed -i -e "s/APP_LAUNCH_SCRIPTNAME/${APP_LAUNCH_SCRIPTNAME}/g" $APP_INFO_PLIST
sed -i -e "s/APP_NAME/${APP_NAME}/g" $APP_INFO_PLIST
sed -i -e "s/APP_MAIN_ICONNAME/${APP_MAIN_ICONNAME}/g" $APP_INFO_PLIST
sed -i -e "s/APP_BUNDLE_IDENTIFIER/${APP_BUNDLE_IDENTIFIER}/g" $APP_INFO_PLIST
sed -i -e "s/APP_VERSION_NUMBER/${APP_VERSION_NUMBER}/g" $APP_INFO_PLIST
sed -i -e "s/APP_BUNDLE_UNIQUE_SIGNATURE/${APP_BUNDLE_UNIQUE_SIGNATURE}/g" $APP_INFO_PLIST
sed -i -e "s/APP_BUILD_NUMBER/${APP_BUILD_NUMBER}/g" $APP_INFO_PLIST

# Remove temporary file created by the above sed commands.
for f in `ls ${APP_INFO_PLIST}*`; do
    if [ "$f" != "${APP_INFO_PLIST}" ]; then
        echo "Removing temp generated sed file ..."
        rm $f
    fi
done
 
# Temporary dmg archive file.
TEMP_DMG=$DEST_DIR/pack.temp.dmg

# Create the temporary dmg archive.
echo "Creating temporary archive file $TEMP_DMG ..."
VOLUME_NAME="$APP_NAME $APP_VERSION"
hdiutil create \
      -srcfolder "$APP_PACKAGE_DIR" \
      -volname "$VOLUME_NAME" \
      -fs HFS+ \
      -fsargs "-c c=64,a=16,e=16" \
      -format UDRW \
      "$TEMP_DMG"

# Unmount any previously mounted dmg archive of the same name.
if [ -d "/Volumes/$VOLUME_NAME" ]; then
    echo "Unmounting already-mounted volumes with the same name."
    umount "/Volumes/$VOLUME_NAME"*
fi

# Mount the dmg archive.
echo "Mounting temporary archive file $TEMP_DMG ..."
device=$(hdiutil attach -readwrite -noverify -noautoopen "$TEMP_DMG" | \
         egrep '^/dev/' | sed 1q | awk '{print $1}')
echo "Device was mounted as: $device"

echo "Adding the installer background image to the archive ..."
BACKGROUND_IMG_DIR="/Volumes/$VOLUME_NAME/.background"
mkdir "$BACKGROUND_IMG_DIR"
cp "$DMG_BACKGROUND_IMG" "$BACKGROUND_IMG_DIR"


# Use AppleScript to set the visual styles (name of .app must be in
# bash variable "applicationName", use variables for the other
# properties as needed):
echo "Setting properties of the installer image ..."
backgroundPictureName="$DMG_BACKGROUND_IMGNAME"
applicationName="$APP_BUNDLE_NAME"
title="$VOLUME_NAME"

echo '
   tell application "Finder"
     tell disk "'${title}'"
           open
           set current view of container window to icon view
           set toolbar visible of container window to false
           set statusbar visible of container window to false
           set the bounds of container window to {400, 100, 880, 425}
           set theViewOptions to the icon view options of container window
           set arrangement of theViewOptions to not arranged
           set icon size of theViewOptions to 72
           set background picture of theViewOptions to file ".background:'${backgroundPictureName}'"
           make new alias file at container window to POSIX file "/Applications" with properties {name:"Applications"}
           set position of item "'${applicationName}'" of container window to {110, 180}
           set position of item "Applications" of container window to {375, 180}
           close
           open
           update without registering applications
     end tell
   end tell
' | osascript

# Finialize the DMG by setting permissions properly, compressing and
# releasing it:
echo "Updating archive permissions ..."
APP_INSTALL_PACKAGE="$DEST_DIR/$APP_INSTALL_PACKAGE_NAME"
chmod -Rf go-w /Volumes/"${title}"
echo "Synching archive ..."
sync
sync
echo "Detaching device $device ..."
hdiutil detach ${device}
echo "Convert temporary archive to final install package ..."
hdiutil convert "$TEMP_DMG" -format UDZO -imagekey zlib-level=9 -o "${APP_INSTALL_PACKAGE}"

# Do some cleanup
echo "Doing post-cleanup..."

echo "Removing temporary dmg file..."
rm -f "$TEMP_DMG"

#echo "Removing working app package directory..."
#rm -rf "$APP_PACKAGE_DIR"

echo "Removing cx_Freeze working directory..."
rm -rf "$CXFREEZE_INSTALL_DIR"

echo "Clean-up complete."
echo ""
echo "Installer archive is now created at location: "
echo "$TOPLEVEL_DIR/$APP_INSTALL_PACKAGE"

#echo "Done."
exit 0 
