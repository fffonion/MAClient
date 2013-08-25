import maClient
import os
import ma
import random
loc='tw'
maClient1=maClient.maClient(savesession=True)
maClient1.initplayer(open(r'D:\Dev\Python\Workspace\binary-works\MA\.%s.playerdata'%loc).read())
maClient1.loc=loc
cardlist=[i for i in maClient1.carddb]
random.shuffle(cardlist)
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
        dt=ma.decode_res(maClient1.download_card(i,j))
        open('e:\\ma\\%s_%d.png'%(i,j),'wb').write(dt)
fuckall()