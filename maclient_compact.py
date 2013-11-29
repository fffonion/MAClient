#!/usr/bin/env python
# coding:utf-8
# maclient compatibility tool
# Contributor:
#      fffonion        <fffonion@gmail.com>
import os
import os.path as opath
import sys
import locale
PYTHON3= sys.version.startswith('3')
IRONPYTHON= sys.platform=='cli'
EXEBUNDLE=opath.split(sys.argv[0])[1].find('py') == -1

getPATH0=(not EXEBUNDLE or IRONPYTHON) and \
     (PYTHON3 and \
        sys.path[0] #python3
        or sys.path[0].decode(sys.getfilesystemencoding())
     ) \
     or sys.path[1].decode(sys.getfilesystemencoding())#pyinstaller build

du8=(IRONPYTHON or PYTHON3) and \
    (lambda str:str) or \
    (lambda str:str.decode('utf-8'))

raw_inputd= PYTHON3 and \
        (lambda s:input(s.encode(locale.getdefaultlocale()[1] or 'utf-8', 'replace')).encode('utf-8')) \
    or \
        (lambda s:raw_input(du8(s).encode(locale.getdefaultlocale()[1] or 'utf-8')).decode(locale.getdefaultlocale()[1] or 'utf-8').encode('utf-8'))