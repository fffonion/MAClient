#!/usr/bin/env python
# coding:utf-8
# merge logs maclient generated
# Contributor:
#      fffonion        <fffonion@gmail.com>

#using sort
#sort -m -t "" -k 1 -o events_merge.log logfile1 logfile2 ...
import os
import re
import sys
import time

try:
    files=sys.argv[1:]
    sys.argv[1]
except IndexError:
    print('Usage: log_merge.py logfile1 logfile2 ... \n\toutput will be written into "events_merge.log"')
    sys.exit(1)

flines=[]
for f in files:
    try:
        flines.append(open(f,'r').readlines())
    except IOError():
        print('file %s not found'%f)
        sys.exit(1)

def get_time(str):
    strtime=str[1:str.find(']')]
    return time.strptime(strtime,'%b %d %X')

merge_lines=[]
index=[0]*len(files)
while True:
    early='[Dec 31 23:59:59]'
    ind=0
    finish=True
    for i in range(len(files)):
        if index[i]==len(flines[i]):
            continue
        else:
            finish=False
        try:
            if get_time(flines[i][index[i]])<get_time(early):
                early=flines[i][index[i]]
                ind=i
        except ValueError:#没时间数据，直接转移
            early=flines[i][index[i]]
            ind=i
    if finish:
        break
    index[ind]+=1
    if early not in merge_lines:#重复检测
        merge_lines.append(early)
open('events_merge.log','w').write(''.join(merge_lines))