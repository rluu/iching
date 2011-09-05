##############################################################################
# NSIS script for creating an installer exe for installing I Ching
##############################################################################

# Include the header file for Modern UI 2.
!include MUI2.nsh

##############################################################################
# General settings.

# Name and file.
Name "I Ching"
OutFile "iching-installer-win32-v1.0.5.exe"

# Default installation directory.
InstallDir "$LOCALAPPDATA\I Ching"

# Get installation directory from registry if available.
InstallDirRegKey HKCU "Software\I Ching" ""

# Request application privileges for execution.
RequestExecutionLevel user

##############################################################################
# Variables

Var StartMenuFolder

##############################################################################
# Interface Settings

!define MUI_ABORTWARNING

##############################################################################
# Pages

# Installer pages.
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "doc/LICENSE.txt"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY

# Start menu folder page configuration.
!define MUI_STARTMENUPAGE_REGISTRY_ROOT "HKCU"
!define MUI_STARTMENUPAGE_REGISTRY_KEY "Software\I Ching"
!define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "Start Menu Folder"

!insertmacro MUI_PAGE_STARTMENU Application $StartMenuFolder

!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

# Uninstaller pages.
!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

##############################################################################
# Languages

!insertmacro MUI_LANGUAGE "English"

##############################################################################
# Installer Section

Section "I Ching Application" SecMain
 
    # Set the installation directory as the destination for the 
    # following actions.
    SetOutPath "$INSTDIR"

    # Files to install.
    File /r /x .svn "conf"
    File /r /x .svn "dist"
    File /r /x .svn "doc"
    File /r /x .svn /x *.svg /x Makefile* "resources"

    # Create log directory.
    CreateDirectory "$INSTDIR\logs"

    # Store installation folder.
    WriteRegStr HKCU "Software\I Ching" "" $INSTDIR

    # Create the uninstaller.
    WriteUninstaller "$INSTDIR\Uninstall.exe"
 
    !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
        # Create shortcuts.
        CreateDirectory "$SMPROGRAMS\$StartMenuFolder"

        # Create a shortcut in the start menu folder for running the 
        # application.
        CreateShortCut "$SMPROGRAMS\$StartMenuFolder\I Ching.lnk" "$INSTDIR\dist\main.exe" "" "$INSTDIR\resources\images\rluu\appIcon.ico"

        # Create a shortcut in the start menu folder for uninstalling.
        CreateShortCut "$SMPROGRAMS\$StartMenuFolder\Uninstall.lnk" "$INSTDIR\Uninstall.exe"

    !insertmacro MUI_STARTMENU_WRITE_END

SectionEnd
 
##############################################################################
# Uninstaller Section

Section "Uninstall"
 
    # Remove installation directory.
    RMDir /r "$INSTDIR"

    # Remove the start menu folder and all its contents 
    # (including short-cut links).
    RMDir /r "$SMPROGRAMS\$StartMenuFolder"


    # Delete the registry key.
    DeleteRegKey /ifempty HKCU "Software\I Ching"

# Uninstaller section end.
SectionEnd
