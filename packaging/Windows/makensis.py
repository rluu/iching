#!/usr/bin/env python3
##############################################################################
# File: makensis.py
#
# Description:
#
#     Basically just a wrapper script that looks for the NSIS path in
#     the Windows registry, and then invokes makensis.exe with the
#     arguments to this script.
#
##############################################################################

import os
import subprocess
import sys

from optparse import OptionParser

from winreg import *

##############################################################################

class RegistryValue():
    """Class that can hold the tuple values that come out of a call to
    winreg.EnumValue(key, index)
    """

    def __init__(self, name="", value=None, dataType=None):
        self.name = name
        self.value = value
        self.dataType = dataType

##############################################################################

def getNsisPath():
    """Looks in the Registry to find the Nsis path.  If it was unable to find
    the path, then an empty string is returned.
    """

    print("Connecting to Registry...")
    aReg = ConnectRegistry(None,HKEY_LOCAL_MACHINE)
    
    print("Connected to Registry.")
    
    registryKey = "Software\\NSIS"
    
    print("Opening key: {}".format(registryKey))
    aKey = OpenKey(aReg, registryKey)
    
    
    # List holding registry values at this key.
    registryValues = []
    
    # Get all teh registry values at this key, as RegistryValue objects and
    # append them to the registryValues list.
    for i in range(1024):
        try:
            n,v,t = EnumValue(aKey,i)
            print("i={}, n={}, v={}, t={}".format(i, n, v, t))
            regVal = RegistryValue(name=n, value=v, dataType=t)
            registryValues.append(regVal)
        except EnvironmentError:                                               
            print("Found {} total key values.".format(i))
            break
    
    #print("Closing key: {}".format(registryKey))
    CloseKey(aKey)
    
    # Find the NSIS path.
    for regVal in registryValues:
        if regVal.name == "" and regVal.dataType == 1:
            nsisPath = regVal.value
            print("nsisPath is: " + nsisPath)
            return nsisPath

    return ""



def parseCommandlineArgs():
    """Parses the command-line arguments passed to this script.
    Returns the options and arguments as a tuple: (options, args)
    """

    parser = OptionParser()
    
    parser.add_option("-f", "--file",
                      action="store",
                      type="string",
                      dest="inputFile",
                      default="",
                      help="Specify NSIS configuration script (.nsi file) " + \
                           "to process with makensis.exe",
                      metavar="<NSIS_FILE>")

    (options, args) = parser.parse_args()

    if options.inputFile == "":
        print("Error: No input file was specified." + os.linesep)
        parser.print_help()
        sys.exit(1)

    return (options, args)


def main():
    # Parse command-line arguments.
    (options, args) = parseCommandlineArgs()

    # Return value.
    rv = 0

    if options.inputFile != "":
        if not os.path.isfile(options.inputFile):
            print("Error: File specified is invalid.")
            sys.exit(1)
        else:
            makeNsisExeStr = "makensis.exe"
            nsisPath = getNsisPath()

            executable = nsisPath + os.sep + makeNsisExeStr
            rv = subprocess.call([executable, options.inputFile])
            print("Subprocess completed.  " + \
                  makeNsisExeStr + " returned " + str(rv))
        
    sys.exit(rv)

##############################################################################

if __name__ == "__main__":
    main()

##############################################################################

