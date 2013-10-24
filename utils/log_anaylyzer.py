#!/usr/bin/env python
# coding:utf-8
# log analyzer
# Contributor:
#      fffonion        <fffonion@gmail.com>

#using sort
#sort -m -t "" -k 1 -o events_merge.log logfile1 logfile2 ...
import os
import re
import sys

try:
    lfile=sys.argv[1]
    sys.argv[1]
except IndexError:
    print('Usage: log_analyzer.py logfile')
    sys.exit(1)

def data_add(dic,key,val):
    val=float(val)
    if key in dic:
        dic[key][0]=(dic[key][0]*dic[key][1]+val)/(dic[key][1]+1)
        dic[key][1]+=1
    else:
        dic[key]=[val,1]

fairys={}
'''妖精:波寇Lv13 hp:157320 发现者:fffonion 小伙伴:0'''
pending_fairy=None
lines=open(lfile).readlines()
for ind in range(len(lines)):
    line_ori=lines[ind]
    #print line_ori.decode('utf-8').encode('cp936','ignore')
    line=line_ori[18:]
    if line.startswith('妖精:'):
        fname=re.findall('妖精:([^L]+)',line)[0]
        try:
            lv=re.findall('Lv(\d+)',line)[0]
        except IndexError:
            continue
        #print fname.decode('utf-8').encode('cp936'),fname not in fairys
        #raw_input()
        if fname not in fairys:
            fairys[fname]={}
        try:
            nakama=re.findall('小伙伴:(\d+)',line)[0]
        except IndexError:
            pass#broken log
        else:
            if nakama=='0':#is full hp
                #data_add(fairys[fname],'HP,%s'%lv,re.findall('hp:(\d+)',line)[0])
                if 'HP,%s'%lv not in fairys[fname]:#record the first time
                    fairys[fname]['HP,%s'%lv]=[float(re.findall('hp:(\d+)',line)[0]),1]
            pending_fairy=[fname,lv,0]
    if pending_fairy:
        if line_ori.startswith('ROUND:'):
            fname,lv=pending_fairy[:2]
            atk=re.findall('ATK\:[\d\.]+\/([\d\.]+)',line_ori)[0]
            if atk!='0.0':
                data_add(fairys[fname],'ATK,%s'%lv,atk)
            pending_fairy=None
        else:
            if pending_fairy[-1]>=20:#过了20行
                pending_fairy=None
            else:
                pending_fairy[-1]+=1
f=open(r'z:\output.csv','w')
for fa in fairys:
    f.write(fa.decode('utf-8').encode('gbk')+'\n')
    for i in sorted(fairys[fa].items(),key=lambda x:(x[0].split(',')[0],int(x[0].split(',')[1]))):
        f.write('%s,%s\n'%(i[0],round(i[1][0],1)))
