#!/usr/bin/env python
# coding:utf-8
# merge logs maclient generated
# Contributor:
#      fffonion        <fffonion@gmail.com>

# using sort
# sort -m -t "" -k 1 -o events_merge.log logfile1 logfile2 ...
import os
import re
import sys

try:
    files = sys.argv[1:]
    sys.argv[1]
except IndexError:
    print('Usage: log_merge.py logfile1 logfile2 ... \n\toutput will be written into "events_merge.log"')
    sys.exit(1)

flines = []
for f in files:
    try:
        flines.append(open(f, 'r').readlines())
    except IOError():
        print('file %s not found' % f)
        sys.exit(1)

cache_d = {}
def cache(func):
    def __decorator(key):  # add parameter receive the user information
        if key in cache_d:
            return cache_d[key]
        else:
            r = func(key)
            cache_d[key] = r
            return r
    return __decorator

mon = 'JanFebMarAprMayJunJulAugSepOctNovDec'
def timefmt(t):
    m = mon.find(t[:3])
    return [m, t[4:6], t[7:9], t[10:12], t[13:]]

@cache
def get_time(strt):
    if strt.startswith('['):
        if strt.find(']') != 16:  # malformed
            end = strt.find(']')
            strt = strt[end - 15:end]
        strtime = strt[1:16]
        return timefmt(strtime)
    else:  # 没时间数据,返回一个最小的时间
        return [0, '01', '00', '00', '01']


merge_lines = []
index = [0] * len(files)
while True:
    early = '[Dec 31 23:59:59]'
    ind = 0
    finish = True
    for i in range(len(files)):
        if index[i] == len(flines[i]):  # EOF
            continue
        else:
            finish = False
            if get_time(flines[i][index[i]]) <= get_time(early):
                # print get_time(flines[i][index[i]]),get_time(early),i
                # raw_input()
                early = flines[i][index[i]]
                ind = i
    if finish:
        break
    index[ind] += 1
    if early not in merge_lines or not early.startswith('['):  # 重复检测
        merge_lines.append(early)
open('events_merge.log', 'w').write(''.join(merge_lines))
