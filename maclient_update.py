#!/usr/bin/env python
# coding:utf-8
# maclient master data updater
# Contributor:
#      fffonion        <fffonion@gmail.com>
import os
import os.path as opath
import sys
from xml2dict import XML2Dict

getPATH0=(opath.split(sys.argv[0])[1].find('py') != -1 or sys.platform=='cli') \
     and sys.path[0].decode(sys.getfilesystemencoding()) \
     or sys.path[1].decode(sys.getfilesystemencoding())#pyinstaller build

def get_revision(loc):
    loc=loc[:2]
    local_revs=open(opath.join(getPATH0,'db/revision.txt')).read().split('\n')
    rev=None
    for r in local_revs:
        r=r.split(',')
        if r[0]==loc:
            rev=r
            break
    if not rev:
        raise KeyError('No server revision data found for "%s"'%loc)
    return rev[1:]

def save_revision(loc,cardrev=None,itemrev=None):
    rev_str=open(opath.join(getPATH0,'db/revision.txt')).read()
    local_revs=rev_str.split('\n')
    rev=None
    for r in local_revs:
        rl=r.split(',')
        if rl[0]==loc:
            rev=rl
            break
    if not rev:
        raise KeyError('No server revision data found for "%s"'%loc)
    if cardrev:
        rev[1]=str(cardrev)
    if itemrev:
        rev[2]=str(itemrev)
    rev_str=rev_str.replace(r,','.join(rev))
    open(opath.join(getPATH0,'db/revision.txt'),'w').write(rev_str)

def check_revision(loc,rev_tuple):
    rev=get_revision(loc)
    if rev:
        return rev_tuple[0]>float(rev[0]),rev_tuple[1]>float(rev[1])
    else:
        return False,False

def update_master(loc,need_update,poster):
    new_rev=[None,None]
    if need_update[0]:
        a,b=poster.post('masterdata/card/update',postdata='%s&revision=0'%poster.cookie,noencrypt=True)
        resp=XML2Dict().fromstring(b.replace('&','--').replace('--#','&#')).response#不替换会解析出错摔
        cards=resp.body.master_data.master_card_data.card
        strs=[]
        for c in cards:
            strs.append('%s,%s,%s,%s,%s,%s,%s,%s'%(
                c.master_card_id,
                c.name.replace('--','&'),
                c.rarity,
                c.cost,
                str(c.char_description).strip('\n').strip(' ').replace('\n','\\n'),
                c.skill_kana,
                c.skill_name,
                str(c.skill_description).replace('\n','\\n')))
        open(opath.join(getPATH0,'db/card.%s.txt'%loc),'w').write('\n'.join(strs))
        new_rev[0]=resp.header.revision.card_rev
        save_revision(loc,cardrev=new_rev[0])
    if need_update[1]:
        a,b=poster.post('masterdata/item/update',postdata='%s&revision=0'%poster.cookie,noencrypt=True)
        resp=XML2Dict().fromstring(b).response
        itmes=resp.body.master_data.master_item_data.item_info
        strs=[]
        for c in itmes:
            strs.append('%s,%s,%s'%(
                c.item_id,
                c.name,
                c.explanation
            ))
        open(opath.join(getPATH0,'db/item.%s.txt'%loc),'w').write('\n'.join(strs))
        new_rev[1]=resp.header.revision.item_rev
        save_revision(loc,itemrev=new_rev[1])
    return new_rev    