#!/usr/bin/env python
# coding:utf-8
# maclient compatibility tool
# Contributor:
#      fffonion        <fffonion@gmail.com>
from __future__ import print_function
import os
import os.path as opath
import sys
import locale
PYTHON3 = sys.version.startswith('3')
IRONPYTHON = sys.platform == 'cli'
EXEBUNDLE = hasattr(sys, 'argv') and opath.split(sys.argv[0])[1].find('py') == -1
LOCALE = locale.getdefaultlocale()[0]
CODEPAGE = locale.getdefaultlocale()[1]
NICE_TERM = 'NICE_TERM' in os.environ

try:
    import bae.core
except ImportError:
    BAE = False
else:
    BAE = True
try:
    import sae
except ImportError:
    SAE = False
else:
    SAE = True
OPENSHIFT = 'OPENSHIFT_PYTHON_IP' in os.environ

BOT = True
if BOT or BAE or SAE or OPENSHIFT:
    print = lambda x:x

print = lambda x:x
convhans = lambda x:x
try:
    import ZhConversion
except ImportError:
    pass
else:
    chans = ZhConversion.convHans()
    if LOCALE == 'zh_TW':
        convhans = chans.toTW
    elif LOCALE == 'zh_HK':
        convhans = chans.toHK

getPATH0 = SAE and '' or ((not EXEBUNDLE or IRONPYTHON) and \
     (PYTHON3 and \
        sys.path[0]  # python3
        or sys.path[0].decode(sys.getfilesystemencoding())
     ) \
     or sys.path[1].decode(sys.getfilesystemencoding()))  # pyinstaller build

raw_du8 = (IRONPYTHON or PYTHON3) and \
    (lambda str:str) or \
    (lambda str:convhans(str).decode('utf-8'))

raw_convstr = (sys.platform.startswith('cli') or PYTHON3 or NICE_TERM)and \
        (lambda str: str) or \
        (lambda str: str.decode('utf-8').encode(locale.getdefaultlocale()[1] or 'utf-8', 'replace'))

du8 = lambda x: raw_convstr(raw_du8(x))

raw_inputd = PYTHON3 and \
        (lambda s:input(s)) \
    or \
        (lambda s:raw_input(du8(s).encode(CODEPAGE or 'utf-8')).decode(CODEPAGE or 'utf-8').encode('utf-8'))
        
# from goagent.appcfg
def _win_getpass(prompt='Password:', stream=None):
    password = ''
    sys.stdout.write(prompt)
    while 1:
        ch = msvcrt.getch()
        if ch == '\b':
            if password:
                password = password[:-1]
                sys.stdout.write('\b \b')
            else:
                continue
        elif ch == '\r':
            sys.stdout.write(os.linesep)
            return password
        else:
            password += ch
            sys.stdout.write('*')

try:
    import msvcrt
    getpass = _win_getpass
except ImportError:
    import getpass
    getpass = getpass.getpass

