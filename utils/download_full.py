import os
import random
import httplib2
import sys
sys.path.append(os.path.abspath('..'))
import maclient_player
import maclient_network
os.chdir(os.path.abspath('..'))
sys.path[0]=os.path.abspath('.')
CARD_NORM,CARD_MAX,CARD_NORM_HOLO,CARD_MAX_HOLO=0,1,2,3
ht=httplib2.Http()

def gen_list(loc):
    p=maclient_player.player(open(r'D:\Dev\Python\Workspace\maclient\.tw.playerdata').read(),loc)
    cardlist=[i for i in p.card.db]
    random.shuffle(cardlist)
    return cardlist,p.card.db


def download_card(cardid,level=CARD_NORM):
        #print serv['%s_data'%self.loc]+uri['%s_data_card'%loc]+uri['cardlevel'][level]%cardid
        rev={'cn_card':172,'tw_card':173}
        card={'cn_data_card':'MA/PROD/%d/'%rev['cn_card'],'tw_data_card':'contents/%d/'%rev['tw_card'],\
        'cardlevel':\
            ['card_full/full_thumbnail_chara_%d?cyt=1','card_full_max/full_thumbnail_chara_5%03d?cyt=1',\
            'card_full_h/full_thumbnail_chara_%d_horo?cyt=1','card_full_h_max/full_thumbnail_chara_5%03d_horo?cyt=1']
        }
        resp,content=ht.request(maclient_network.serv['%s_data'%loc]+card['%s_data_card'%loc]+card['cardlevel'][level]%cardid,\
                method='GET',headers={'ua':'Million/100','accept':'gzip','connection':'keep-alive'})
        return content
def fuckall():
    clst,cname=gen_list(loc)
    tlst=gen_list('tw')[0]
    pct=0.0
    while pct!=100:
        for i in clst:
            if int(i) in xrange(161,171):
                continue 
            if i in tlst:
                print i
                continue
            j=random.choice([0,1,2,3])
            time=0
            print i,'->',j,
            while os.path.exists('%s%s-%s_%d.png'%(download_dir,cname[i][0].decode('utf-8'),i,j)) and time<3:
                j=(j+3)%4
                time+=1
                print j,
            if time ==3:
                print ''
                continue
            pct=100.00*len(os.listdir(download_dir))/4/len(clst)
            print pct,'%'
            a=download_card(i,j)
            if len(a)%16:
                continue
            dt=maclient_network.decode_res(a)
            open('%s%s-%s_%d.png'%(download_dir,cname[i][0].decode('utf-8'),i,j),'wb').write(dt)
loc='cn'
download_dir='e:\\ma\\cn\\'
fuckall()