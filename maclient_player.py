#!/usr/bin/env python
# coding:utf-8
# maclient player class
# Contributor:
#      fffonion        <fffonion@gmail.com>
import os
import os.path as opath
import sys
import glob
import time

from xml2dict import XML2Dict

class player(object):
	def __init__(self,login_xml,loc):
		#[:2]可以让cn2变成cn以使用同一个卡组/道具数据
		self.card=card(loc[:2])
		self.item=item(loc[:2])
		self.update_all(login_xml)
		self.loc=loc
		self.fairy={'id':0,'alive':False}
		object.__init__(self)

	def update_all(self,xmldata):
		if xmldata=='':
			return '',False
		else:
			res=[self._update_data(xmldata),self._update_card(xmldata),self._update_item(xmldata)]
			return '%s %s %s'%(res[0][0],res[1][0],res[2][0]),res[1][1]

	def calc_ap_bc(self):
		#正常计算AP BC 变动
		for key in ['ap','bc']:
			if self.hasattr(key):
				getattr(self,key)['current']+=(time.time()-int(getattr(self,key)['current_time']))/int(getattr(self,key)['interval_time'])
				if getattr(self,key)['current']>=getattr(self,key)['max']:
					getattr(self,key)['current']=getattr(self,key)['max']

	def _update_data(self,xmldata):
		self.calc_ap_bc()
		try:
			xml = XML2Dict().fromstring(xmldata)
			if 'login' in xml.response.body:
				self.id=xml.response.body.login.user_id
			else:
				self.id='0'
			self.playerdata=xml.response.header.your_data
		except:
			
			return 'Profile no update',False
		else:
			for key in ['ap','bc']:
				self.__setattr__(key,{})
				for attr in self.playerdata[key]:
					getattr(self,key)[attr]=int(self.playerdata[key][attr].value)
			for key in ['gold','friendship_point']:
				self.__setattr__(key,int(self.playerdata[key].value))
			self.lv=self.playerdata['town_level'].value
			self.leader_sid=self.playerdata['leader_serial_id'].value
			self.name=self.playerdata['name'].value
			#print self.ap.current,self.bc.current
			return 'AP:%d/%d BC:%d/%d G:%d FP:%d '%(self.ap['current'],self.ap['max'],self.bc['current'],self.bc['max'],self.gold,self.friendship_point),True

	def _update_card(self,xmldata):
		try:
			xml = XML2Dict().fromstring(xmldata)
			self.card.update(xml.response.header.your_data.owner_card_list.user_card)
			return 'CARDs:%d'%self.card.count,True
		except :
			return '',False

	def _update_item(self,xmldata):
		try:
			xml = XML2Dict().fromstring(xmldata)
			self.item.update(xml.response.header.your_data.itemlist)
			return 'Items updated',True
		except:
			return '',False
	def hasattr(self,key):
		try:
			getattr(self,key)
		except AttributeError:
			return False
		else:
			return True
	def __setattr__(self,key,val):
		return object.__setattr__(self,key,val)

class item(object):
	def __init__(self,loc):
		self.getPATH0=lambda:opath.split(sys.argv[0])[1].find('py') != -1\
		 and sys.path[0].decode(sys.getfilesystemencoding()) \
		 or sys.path[1].decode(sys.getfilesystemencoding())#pyinstaller build
		self.name={}
		for c in open(opath.join(self.getPATH0(),'db/item.%s.txt'%loc)).read().split('\n'):
			c=c.split(',')
			if c!=['']:
				self.name[int(c[0])]=c[1]
		self.count={}
	def update(self,itemdict):
		for it in itemdict:
			try:
				self.count[int(it.item_id)]=it.num
			except KeyError:
				self.count[int(it.item_id)]='0'


class card(object):
	def __init__(self,loc):
		self.getPATH0=lambda:opath.split(sys.argv[0])[1].find('py') != -1\
		 and sys.path[0].decode(sys.getfilesystemencoding()) \
		 or sys.path[1].decode(sys.getfilesystemencoding())#pyinstaller build
		self.db={}
		for c in open(opath.join(self.getPATH0(),'db/card.%s.txt'%loc)).read().split('\n'):
			c=c.split(',')
			if c!=['']:
				self.db[int(c[0])]=[c[1],int(c[2]),int(c[3])]
		self.count=0
	
	def update(self,carddict):
		self.cards=carddict
		self.count=len(self.cards)
		#print self.cid('124')
	def _found_card_by_value(self,key,value):
		res=[]
		for i in self.cards:
			if i[key].value==value:
				res.append(i)
		return res
	def sid(self,sid):
		return self._found_card_by_value('serial_id',sid)[0]
	def cid(self,cid):
		return self._found_card_by_value('master_card_id',cid)


if __name__=='__main__':
	if len(sys.argv)>2:
		input_path=sys.argv[1]#.replace("\\","\\\\")
		output_dir=sys.argv[2]#.replace("\\","\\\\")
	else:
		input_path=r'E:\ACG\GameArchive\MA\com.square_enix.million_tw\files\save\download'
		output_dir-r'E:\ACG\GameArchive\MA\com.square_enix.million_tw\files\save\decrypt'
	filelist=[]
	if os.path.isdir(input_path):
		for root,dirs,files in os.walk(input_path):
			for f in files:
				filelist.append(os.path.join(root,f))
	else:
		filelist=[input_path]
	for i in filelist:
		if not os.path.isdir(i):
			save=i.replace(os.path.split(input_path)[0],output_dir)
			decrypt_file(i,save)
	# #import binascii
	# #hexlify=lambda x: binascii.hexlify(x)
	# print decode_param('S=tAS5lPt7ftw8HlSUflkJFA%3D%3D%0A&login_id=8lIlKXItI6T3p7zAORJJSw%3D%3D%0A&password=v%2FCxxyFKqD5NahTXKACSkg%3D%3D%0A&app=dpa7%2FriPmmGftWfXGdEv2Q%3D%3D%0A&token=fRqY08WorSorOWR8188aGceoMhi1v5NUjKV9Vu4SspgVyyotBRSo%2Bj%2FpYH3NxSS5p96kBK2%2FQz2N%0AGmf0rHmspgT9DiDBH4wkSvpAJdbRExFM8yxS41SPimTpl99QmVCv0fhSOV8Kztx9eseMD4jbWbcU%0AXthkY4ALLLFdZ3xpnJbpOxFiQku6Ovyw0MnSG4dxDsy4n6ybmIrPin3W%2BSU%2FLr7Wk0s5RXJF3iTI%0AQDTmN1SGmmZM1kqReNhMdx74EiYxvRXr51EsPJEvDSPfu%2F542DM2By584uiANhpify5iFRXZisI7%0AyGZp8QGNr1NIego5aBG8KsXmX%2BgzcaAx3wL8nw%3D%3D%0A')
	# #print decode_param('notice_id=bfOK21o6f0flO9OlO1dRkByUK8bPymhd4cjvNVkto3Q%3D%0A')
	# #area_id=90115
	# #area_id=90115%0A&check=1%0A&floor_id=3
	# #area_id=90115%0A&auto_build=1%0A&floor_id=3
	# import random
	# p='invitation_id=8204a&login_id=%s&param=&password=%s&param=%s'%('goodevening','zcn19920492','35'+(''.join([str(random.randint(0,10)+i-i) for i in range(10)])))
	# print encode_param(p),len(encode_param(p))
	# #Million/100 (Samsung; Gallaxy S; 4.2) generic/Gallaxy S/Gallaxy S:4.2/stock/com.littlewithe.20130402.good/stable-keys
	# #print c.db['cn']['72']
	# #knight_id=0%0A&move=1%0A&parts_id=0
	# #S=nosessionid&login_id=zzh930916&password=19930917&app=and&token=BubYIgiyDYTFUifydHIoIOGBiujgRzrEFUIbIKOHniHIoihoiHasbdhasbdUIUBujhbjhjBJKJBb
	# #59247865
	# #xmld=open(r'D:\Dev\Python\Workspace\binary-works\MA\login','r').read()
	# #pl=player(xmld)
	# #print pl.card.cid('9999')
	
