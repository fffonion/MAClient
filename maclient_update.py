#!/usr/bin/env python
# coding:utf-8
# maclient master data updater
# Contributor:
#      fffonion        <fffonion@gmail.com>
import os
import os.path as opath
import sys
from xml2dict import XML2Dict
from cross_platform import *

def get_revision(loc):
    loc = loc[:2]
    local_revs = open(opath.join(getPATH0, 'db/revision.txt')).readlines()
    rev = None
    for r in local_revs:
        r = r.split(',')
        if r[0] == loc:
            rev = r
            break
    if not rev:
        raise KeyError('No server revision data found for "%s"' % loc)
    return rev[1:]

def save_revision(loc, cardrev = None, itemrev = None, bossrev = None):
    rev_str = open(opath.join(getPATH0, 'db/revision.txt')).read()
    local_revs = rev_str.split('\n')
    rev = None
    for r in local_revs:
        rl = r.split(',')
        if rl[0] == loc:
            rev = rl
            break
    if not rev:
        raise KeyError('No server revision data found for "%s"' % loc)
    if cardrev:
        rev[1] = str(cardrev)
    if itemrev:
        rev[2] = str(itemrev)
    if len(rev) < 4:#legacy db support
        rev += ['0']
    if bossrev:
        rev[3] = str(bossrev)
    rev_str = rev_str.replace(r, ','.join(rev))
    open(opath.join(getPATH0, 'db/revision.txt'), 'w').write(rev_str)

def check_revision(loc, rev_tuple):
    rev = get_revision(loc) + [0]#legacy db support
    if rev:
        return rev_tuple[0] > float(rev[0]), rev_tuple[1] > float(rev[1]), rev_tuple[2] > float(rev[2])
    else:
        return False, False, False

def update_master(loc, need_update, poster):
    new_rev = [None, None, None]
    if need_update[0]:
        poster.set_timeout(240)
        a, b = poster.post('masterdata/card/update', postdata = '%s&revision=0' % poster.cookie)
        resp = XML2Dict().fromstring(b.replace('&', '--').replace('--#', '&#')).response  # 不替换会解析出错摔
        cards = resp.body.master_data.master_card_data.card
        strs = []
        for c in cards:
            strs.append('%s,%s,%s,%s,%s,%s,%s,%s' % (
                c.master_card_id,
                c.name.replace('--', '&'),
                c.rarity,
                c.cost,
                str(c.char_description).strip('\n').strip(' ').replace('\n', '\\n'),
                c.skill_kana,
                c.skill_name,
                str(c.skill_description).replace('\n', '\\n')))
        if PYTHON3:
            f = open(opath.join(getPATH0, 'db/card.%s.txt' % loc), 'w', encoding = 'utf-8').write('\n'.join(strs))
        else:
            f = open(opath.join(getPATH0, 'db/card.%s.txt' % loc), 'w').write('\n'.join(strs))
        new_rev[0] = resp.header.revision.card_rev
        save_revision(loc, cardrev = new_rev[0])
    if need_update[1]:
        poster.set_timeout(240)
        a, b = poster.post('masterdata/item/update', postdata = '%s&revision=0' % poster.cookie)
        resp = XML2Dict().fromstring(b).response
        items = resp.body.master_data.master_item_data.item_info
        strs = ['%s,%s,%s' % (
                c.item_id,
                c.name,
                c.explanation.replace('\n','\\n')
            ) for c in items] + ['']
        if PYTHON3:
            open(opath.join(getPATH0, 'db/item.%s.txt' % loc), 'w', encoding = 'utf-8').write('\n'.join(strs))
        else:
            open(opath.join(getPATH0, 'db/item.%s.txt' % loc), 'w').write('\n'.join(strs))
        new_rev[1] = resp.header.revision.item_rev
        save_revision(loc, itemrev = new_rev[1])
    if need_update[2]:
        poster.set_timeout(240)
        a, b = poster.post('masterdata/boss/update', postdata = '%s&revision=0' % poster.cookie)
        resp = XML2Dict().fromstring(b).response
        boss = resp.body.master_data.master_boss_data.boss
        strs = ['%s,%s,%s' % (
                c.master_boss_id,
                c.name,
                c.hp
            ) for c in boss] + ['']
        if PYTHON3:
            open(opath.join(getPATH0, 'db/boss.%s.txt' % loc), 'w', encoding = 'utf-8').write('\n'.join(strs))
        else:
            open(opath.join(getPATH0, 'db/boss.%s.txt' % loc), 'w').write('\n'.join(strs))
        new_rev[2] = resp.header.revision.boss_rev
        save_revision(loc, bossrev = new_rev[2])
    poster.set_timeout(15)#rollback
    return new_rev
