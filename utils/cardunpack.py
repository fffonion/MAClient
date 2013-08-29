#coding:utf-8
#A tool to unpack master_card file to csv
from __future__ import print_function
import os,os.path as opth
import sys
import binascii
import struct
reload(sys)
sys.setdefaultencoding('utf-8')
dt=open(r'z:\master_card','rb').read()
curpos=dt.find(b'\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00')+8#卡组数据开始，第一张为兰斯洛特
nextpos=0
intl=lambda x:[str(int(binascii.hexlify(i),16)) for i in x]
while nextpos!=-1 and curpos<=len(dt):
    card_info=['',]*9
    #00x3 [cid] 00 00 00 01 00 00 00 [名称] 00 00 01 [描述] 00 00 00  [COMBO_EN] 00 00 00 [COMBO_CN] 00 00 00[COMBO_DESC]
    #00 00 00 [ILLUST] 00 00 00 [cost] 00 00 00 [star] 00x6 [??] 00 00 [??] 00x10 [lv1 hp] 00 00 [lv1 atk] +105bit
    #unicode字符串前一字节要截去(00 00 00后一字节)
    cid=str(int(binascii.hexlify(dt[curpos-6:curpos-4]),16))
    is001=True
    for i in range(1,7):
        nextpos=dt.find(b'\x00\x00\x00',curpos+4)#卡片开始标志
        if i==1 and nextpos-curpos<277:#magic number!
            nextpos=dt.find(b'\x00\x00\x00',nextpos+1)
            is001=False
        print(curpos,nextpos)
        card_info[i]=dt[curpos+4:nextpos]
        #print(card_info[i])
        curpos=nextpos
    curpos-=4
    card_info[0:2]=card_info[1].split(is001 and b'\x00\x00\x01' or b'\x00\x00\x00')
    card_info[1]=card_info[1][1:]
    card_info[6:9]=intl(struct.unpack('>3xc3xc22x2s2x2s',dt[curpos:curpos+36]))
    print(cid+'\n--'.join(card_info).decode('utf-8',errors='replace').encode('gbk',errors='replace'))
    curpos+=150
    #to debug
    if not int(card_info[7]) in xrange(1,7):
        raw_input()
        #print curpos,int(binascii.hexlify(dt[zzz+3]),16),name,desc
    open(r'z:/card.cn.txt','a').write('%s,%s\n'%(cid,','.join([card_info[0],card_info[7],card_info[6]]+card_info[1:5]).replace('\n','\\n')))