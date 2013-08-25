import ma
from xml2dict import XML2Dict
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
dt=ma.decode_data(open(r'z:\test.a','rb').read())
open(r'z:\test.xml','w').write(dt)
xml= XML2Dict().fromstring(dt)
print xml.response.header.error.message.encode('utf-8')
# print info.fairy.name+' lv'+info.fairy.lv+' hp'+info.fairy.hp
# print ' sid '+info.fairy.serial_id+' mid '+info.fairy.master_boss_id+' uid '+info.fairy.discoverer_id
# print xmlexplore.response.body.battle_result.winner
# compcard=info.autocomp_card[-1]
# print compcard.master_card_id,compcard.lv,compcard.exp,compcard.next_exp
# usercard=info.user_card
# print usercard.master_card_id
#/fairybattle: win:get_floor lose:fairy_lose
