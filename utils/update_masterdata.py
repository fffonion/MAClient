#coding:utf-8
#NOW MERGED INTO maclient_update.py
import os
import random
import httplib2
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from xml2dict import XML2Dict
sys.path.append(os.path.abspath('..'))
import maclient
import maclient_logging
os.chdir(os.path.abspath('..'))
sys.path[0]=os.path.abspath('.')

loc='cn'
mac=maclient.maClient(configfile=r'D:\Dev\Python\Workspace\maClient\_mine\config_cn.ini')
mac.login()
a,b=mac._dopost('masterdata/card/update',postdata='%s&revision=0'%mac.poster.cookie,noencrypt=True)
open(r'z:\card.%s.xml'%loc,'w').write(b)
a,b=mac._dopost('masterdata/item/update',postdata='%s&revision=0'%mac.poster.cookie,noencrypt=True)
open(r'z:\item.%s.xml'%loc,'w').write(b)

xml=open(r'z:\card.%s.xml'%loc,'r').read().replace('&','--').replace('--#','&#')
print XML2Dict().fromstring(xml).response.header.revision.card_rev
body=XML2Dict().fromstring(xml).response.body
cards=body.master_data.master_card_data.card
strs=[]
for c in cards:
    strs.append('%s,%s,%s,%s,%s,%s,%s,%s'%(
        c.master_card_id,
        c.name,
        c.rarity,
        c.cost,
        str(c.char_description).strip('\n').strip(' ').replace('\n','\\n'),
        c.skill_kana,
        c.skill_name,
        str(c.skill_description).replace('\n','\\n')))
open(r'z:\card.%s.txt'%loc,'w').write('\n'.join(strs))
xml=open(r'z:\item.%s.xml'%loc,'r').read().replace('&','--').replace('--#','&#')
body=XML2Dict().fromstring(xml).response.body
itmes=body.master_data.master_item_data.item_info
strs=[]
for c in itmes:
    strs.append('%s,%s,%s'%(
        c.item_id,
        c.name,
        c.explanation
    ))
open(r'z:\item.%s.txt'%loc,'w').write('\n'.join(strs))