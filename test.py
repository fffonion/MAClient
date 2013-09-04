import maclient
import os
import maclient_network
import random
import httplib2
CARD_NORM,CARD_MAX,CARD_NORM_HOLO,CARD_MAX_HOLO=0,1,2,3
ht=httplib2.Http()
loc='tw'
maclient1=maclient.maClient(savesession=True,configfile=r'D:\Dev\Python\Workspace\maClient\_mine\config_little.ini')
maclient1.initplayer(open(r'D:\Dev\Python\Workspace\maclient\.%s.playerdata'%loc).read())
maclient1.loc=loc
cardlist=[i for i in maclient1.carddb]
random.shuffle(cardlist)
def download_card(cardid,level=CARD_NORM):
        #print serv['%s_data'%self.loc]+uri['%s_data_card'%loc]+uri['cardlevel'][level]%cardid
        rev={'cn_card':169,'tw_card':171}
        card={'cn_data_card':'MA/PROD/%d/'%rev['cn_card'],'tw_data_card':'contents/%d/'%rev['tw_card'],\
        'cardlevel':\
            ['card_full/full_thumbnail_chara_%d?cyt=1','card_full_max/full_thumbnail_chara_5%03d?cyt=1',\
            'card_full_h/full_thumbnail_chara_%d_horo?cyt=1','card_full_h_max/full_thumbnail_chara_5%03d_horo?cyt=1']
        }
        resp,content=ht.request(maclient_network.serv['%s_data'%loc]+card['%s_data_card'%loc]+card['cardlevel'][level]%cardid,\
                method='GET',headers={'ua':'Million/100','accept':'gzip','connection':'keep-alive'})
        return content
def fuckall():
    for i in cardlist:
        j=random.choice([0,1,2,3])
        time=0
        print i,'->',j,
        while os.path.exists('e:\\ma\\%s_%d.png'%(i,j)) and time<3:
            j=(j+3)%4
            time+=1
            print j,
        if time ==3:
            print ''
            continue
        print 100.00*len(os.listdir('e:\\ma'))/4/len(cardlist),"%"
        a=download_card(i,j)
        if len(a)%16:
            continue
        dt=maclient_network.decode_res(a)
        open('e:\\ma\\%s_%d.png'%(i,j),'wb').write(dt)
fuckall()