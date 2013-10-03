#!/usr/bin/env python
# coding:utf-8
# maclient plugin loader
# Contributor:
#      fffonion        <fffonion@gmail.com>
import os,os.path as opath
import sys
getPATH0=(opath.split(sys.argv[0])[1].find('py') != -1 or sys.platform=='cli') \
         and sys.path[0].decode(sys.getfilesystemencoding()) \
         or sys.path[1].decode(sys.getfilesystemencoding())#pyinstaller build
sys.path.append(opath.join(getPATH0,'plugins'))
#os.chdir(opath.join(getPATH0(),'plugins'))
sys.path[0]=os.path.abspath(opath.join(getPATH0,'plugins'))
def load_plugins():
    import hehe
    hehe.a()

if __name__=='__main__':
    load_plugins