#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from xml2dict import XML2Dict
loc='tw'
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