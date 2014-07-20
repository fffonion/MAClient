#!/usr/bin/env python
# coding:utf-8
# maclient master data updater
# Contributor:
#      fffonion        <fffonion@gmail.com>
import os
import re
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

def save_revision(loc, cardrev = None, itemrev = None, bossrev = None, cborev = None):
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
    if len(rev) < 5:#legacy db support
        rev += ['0']
    if cardrev:
        rev[1] = str(cardrev)
    if itemrev:
        rev[2] = str(itemrev)
    if bossrev:
        rev[3] = str(bossrev)
    if cborev:
        rev[4] = str(cborev)
    rev_str = rev_str.replace(r, ','.join(rev))
    open(opath.join(getPATH0, 'db/revision.txt'), 'w').write(rev_str)

def check_revision(loc, rev_tuple):
    rev = get_revision(loc) + [0, 0]#legacy db support
    if rev:
        return rev_tuple[0] > float(rev[0]), rev_tuple[1] > float(rev[1]), rev_tuple[2] > float(rev[2]), rev_tuple[3] > float(rev[3])
    else:
        return False, False, False, False

def update_master(loc, need_update, poster):
    replace_AND = re.compile('&(?!#)')#no CDATA, sad
    #card, item, boss, combo
    new_rev = [None, None, None, None]
    for s in poster.ht.connections:#cleanup socket pool
        poster.ht.connections[s].close()
    poster.ht.connections = {}
    poster.set_timeout(240)
    if loc == 'jp':
        postdata = ''
    else:
        postdata = '%s&revision=0' % poster.cookie
    if need_update[0]:
        a, b = poster.post('masterdata/card/update', postdata = postdata)
        resp = XML2Dict().fromstring(replace_AND.sub('&amp;', b)).response  # 不替换会解析出错摔
        cards = resp.body.master_data.master_card_data.card
        strs = [('%s,%s,%s,%s,%s,%s,%s,%s' % (
                c.master_card_id,
                c.name,
                c.rarity,
                c.cost,
                str(c.char_description).strip('\n').strip(' '),
                c.skill_kana,
                c.skill_name,
                str(c.skill_description)
              )).replace('\n', '\\n') for c in cards] + ['']
        if PYTHON3:
            f = open(opath.join(getPATH0, 'db/card.%s.txt' % loc), 'w', encoding = 'utf-8').write('\n'.join(strs))
        else:
            f = open(opath.join(getPATH0, 'db/card.%s.txt' % loc), 'w').write('\n'.join(strs))
        new_rev[0] = resp.header.revision.card_rev
        save_revision(loc, cardrev = new_rev[0])
    if need_update[1]:
        a, b = poster.post('masterdata/item/update', postdata = postdata)
        resp = XML2Dict().fromstring(replace_AND.sub('&amp;', b)).response
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
        a, b = poster.post('masterdata/boss/update', postdata = postdata)
        resp = XML2Dict().fromstring(replace_AND.sub('&amp;', b)).response
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
    if need_update[3]:
        a, b = poster.post('masterdata/combo/update', postdata = postdata)
        resp = XML2Dict().fromstring(replace_AND.sub('&amp;', b)).response
        cbo = resp.body.master_data.master_combo_data.combo
        strs = ['%s,%s,%s,%s,%s' % (
                c.id,
                c.name,
                c.effect_id,
                c.effect,
                'req_cards' in c and ('[%s]' % c.req_cards) or (
                'req_num_card' in c and ('%s(%s)' % (c.req_num_card, ('req_form_type' in c and c.req_form_type or ''))) or '')
            ) for c in cbo] + ['']
        if PYTHON3:
            open(opath.join(getPATH0, 'db/combo.%s.txt' % loc), 'w', encoding = 'utf-8').write('\n'.join(strs))
        else:
            open(opath.join(getPATH0, 'db/combo.%s.txt' % loc), 'w').write('\n'.join(strs))
        new_rev[3] = resp.header.revision.combo_rev
        save_revision(loc, cborev = new_rev[3])
    for s in poster.ht.connections:#cleanup socket pool
        poster.ht.connections[s].close()
    poster.ht.connections = {}
    poster.set_timeout(20)#rollback
    return new_rev

def update_multi(loc):
    '''抓多玩倍卡数据
    see utils/duowandb.py'''
    from httplib2 import Http
    import base64
    import time
    ht = Http()
    clist = []
    maxpage = 1
    i = 1
    if loc == 'cn':
        qurl = 'http://db.duowan.com/ma/cn/card/list/%s.html'
        idx = 0
    elif loc == 'tw':
        qurl = 'http://db.duowan.com/ma/card/list/%s.html'
        idx = 1
    else:
        return 0
    def dwb64(str):
        return base64.encodestring(str).replace('=','_3_').rstrip('\n')
    while (i <= maxpage):
        resp, ct = ht.request(qurl % dwb64('{"beishu":"all","p":%d,"sort":"quality.desc"}' % i),
                              headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                        'Accept-Language':'zh-CN',
                                        'Cache-Control':'no-cache',
                                        'Connection':'keep-alive',
                                        'DNT':'1',
                                        'Host':'db.duowan.com',
                                        'Pragma':'no-cache',
                                        'User-Agent':'Mozilla/5.0 AppleWebKit/535.12 (KHTML, like Gecko) Chrome/33.0.1782.121 Safari/535.12'}
                                )
        nav = re.findall('mod-page center.*?</div>', ct, re.DOTALL)[0]
        maxpage = len(re.findall('href', nav)) - 2
        i += 1
        tr = re.findall('tr[^c]*class="even">(.*?)<\/tr', ct, re.DOTALL)
        _error_card = []
        for t in tr:
            mid = re.findall('src="http://img.dwstatic.com/ma/[zh_]*pic/face/face_(\d+).jpg">', t)[0]
            try:
                beishu = re.findall('class="icon([\d\.]+)">', t)[0]#哈哈哈哈
            except IndexError:
                _error_card.append('[%s]%s' % (mid, re.findall('title="([^"]+)"', t)[1]))
            clist.append(','.join([mid, beishu]))
        time.sleep(1.414)
    new = '%s=%s\n' % (loc, ';'.join(clist))
    _f = opath.join(getPATH0, 'db/card.multi.txt')
    if PYTHON3:
        kw = {'encoding' : 'utf-8'}
    else:
        kw = {}
    lines = open(_f, **kw).readlines()
    lines[idx] = new
    open(_f, 'w', **kw).write(''.join(lines))
    if _error_card:
        print(du8('倍卡 %s 无法获得倍率数据，请使用am手动添加' % ','.join(_error_card)))
    return len(clist)