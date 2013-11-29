import sys
sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Lib')
sys.path.append(r'C:\Program Files (x86)\IronPython 2.7')
sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\tools\Scripts')
import clr

clr.AddReference('IronPyCrypto')

clr.AddReference('IronPython')
clr.AddReference('IronPython.Modules')
clr.AddReference('Microsoft.Scripting.Metadata')
clr.AddReference('Microsoft.Scripting')
clr.AddReference('Microsoft.Dynamic')
clr.AddReference('mscorlib')
clr.AddReference('System')
clr.AddReference('System.Data')

#
# adapted from os-path-walk-example-3.py

import os, glob
import fnmatch
import pyc

def doscopy(filename1):
    print filename1
    os.system ("copy %s .\\bin\Debug\%s" % (filename1, filename1))

class GlobDirectoryWalker:
    # a forward iterator that traverses a directory tree

    def __init__(self, directory, pattern="*"):
        self.stack = [directory]
        self.pattern = pattern
        self.files = []
        self.index = 0

    def __getitem__(self, index):
        while 1:
            try:
                file = self.files[self.index]
                self.index = self.index + 1
            except IndexError:
                # pop next directory from stack
                self.directory = self.stack.pop()
                self.files = os.listdir(self.directory)
                self.index = 0
            else:
                # got a filename
                fullname = os.path.join(self.directory, file)
                if os.path.isdir(fullname) and not os.path.islink(fullname) and fullname[-4:]<>'.svn':
                    self.stack.append(fullname)
                if fnmatch.fnmatch(file, self.pattern):
                    return fullname

#Build StdLib.DLL
gb = glob.glob(r".\Lib\*.py")
gb.append("/out:StdLib")    

#print ["/target:dll",]+gb

#pyc.Main(["/target:dll"]+gb)

#Build EXE
gb=["/main:maclient_cli.py","xml2dict.py","maclient.py","maclient_network.py","maclient_smart.py","maclient_player.py","maclient_proxy.py","maclient_update.py","maclient_logging.py","maclient_plugin.py","maclient_compact.py","pyaes.py","D:\Dev\Python\Python27\Lib\__future__.py","/target:exe","/out:maclient_cli","/platform:all"]
pyc.Main(gb)

#CopyFiles to Release Directory
#doscopy("StdLib.dll")
doscopy("maclient_cli.exe")


#Copy DLLs to Release Directory
fl = ["IronPython.dll","IronPython.Modules.dll","Microsoft.Dynamic.dll","Microsoft.Scripting.Debugging.dll","Microsoft.Scripting.dll","Microsoft.Scripting.ExtensionAttribute.dll","Microsoft.Scripting.Core.dll"]
#for f in fl:
#  doscopy(f)