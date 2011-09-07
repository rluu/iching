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

from _winreg import *

#print r"*** Reading from SOFTWARE\Microsoft\Windows\CurrentVersion\Run ***"
print("Connecting to Registry...")
aReg = ConnectRegistry(None,HKEY_LOCAL_MACHINE)

print("Connected to Registry.")

registryKey = "Software\NSIS"

print("Opening key: {}".format(registryKey))

aKey = OpenKey(aReg, registryKey)

#aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run") 

for i in range(1024):
    try:
        n,v,t = EnumValue(aKey,i)
        print("i={}, n={}, v={}, t={}".format(i, n, v, t))
    except EnvironmentError:                                               
        print("You have",i," tasks starting at logon...")
        break

print("Closing key: {}".format(registryKey))
CloseKey(aKey)
print("Done.")
      
##############################################################################
#
#require 'win32/registry'
#
#task :package do
#  nsis_path = Win32::Registry::HKEY_LOCAL_MACHINE.open('Software\NSIS') { |reg_entry| reg_entry.read_s('') }
#
#  Dir.open(File.expand_path(File.dirname(__FILE__))).each do |file|
#    if File.extname(file) == '.nsi'
#      sh "\"#{nsis_path}\\makensis.exe\" #{file}"
#    end
#  end
#end
#
#task :default => [:package]
