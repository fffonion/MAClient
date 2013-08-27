#coding:utf-8
#A tool to scratch card data from duowan db
import httplib2
import re
import base64 as b64
import sys
sys.path.append(r'D:\Dev\Python\Workspace\convHans')
import convHans
selcard='{"p":"%d","quality":"%d","sort":"quality.desc"}'
cardlist={'tw':'http://db.duowan.com/ma/card/list/','cn':'http://db.duowan.com/ma/cn/card/list/'}
regex={'tw':'<img title="([^"]+)" style="height:60px" class="img-rounded" src="http://img.dwstatic.com/ma/pic/face/face_(\d+).jpg">',\
		'cn':'<img title="([^"]+)" style="height:60px" class="img-rounded" src="http://img.dwstatic.com/ma/zh_pic/face/face_(\d+).jpg">',\
		'extra':'width="40px">(.*?)</td'}
dbdir=r'D:\Dev\Python\Workspace\binary-works\MA\\'
ht=httplib2.Http()
reload(sys)
sys.setdefaultencoding('utf-8')
h = convHans.convHans()
for loc in ['tw','cn']:
	print loc
	open(dbdir+'db/card.%s.txt'%loc,'w').write('')
	for j in range(1,7):
		clist=[]
		maxpage=4
		i=1
		while (i<=maxpage):
			resp,ct=ht.request(cardlist[loc]+b64.encodestring(selcard%(i,j)).strip('\n').replace('=','_3_')+'.html')
			nav=re.findall('mod-page center.*?</div>',ct,re.DOTALL)[0]
			maxpage=len(re.findall('href',nav))-2
			print i,maxpage,j
			i+=1
			tr=re.findall('tr[^c]*class="even">(.*?)<\/tr',ct,re.DOTALL)
			for t in tr:
				res1=re.findall(regex[loc],t)
				res2=re.findall(regex['extra'],t)[1]
				clist.append([res1[0][0],res1[0][1],res2])
		for i in clist:
			open(dbdir+'db/card.%s.txt'%loc,'a').write(h.toCN(i[1]+','+i[0]+','+str(j)+','+i[2]+'\n', encoding = 'utf-8'))