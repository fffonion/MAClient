#coding:utf-8
#A tool to unpack master_item file to csv
import os,os.path as opth
import sys
import binascii
reload(sys)
sys.setdefaultencoding('utf-8')
dt=open(r'z:\master_item','rb').read()
curpos=0
zzz=0
while zzz!=-1:
	zzz=dt.find(b'\x00\x00\x00',curpos)
	if dt[zzz:zzz+4]==dt[zzz+4:zzz+8]:
		z2=dt.find(b'\x00\x00\x00',zzz+12)
		z3=dt.find(b'\x00\x00\x00',z2+1)
		print zzz,z2,z3
		name=dt[zzz+12:z2].decode('utf-8')
		desc=dt[z2+4:z3].decode('utf-8')
		#print curpos,int(binascii.hexlify(dt[zzz+3]),16),name,desc
		open(r'z:/item.tw.txt','a').write(','.join([str(int(binascii.hexlify(dt[zzz+3]),16)),name,desc])+'\n')
	curpos=zzz+1