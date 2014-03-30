# coding:utf-8
from __future__ import print_function
from _prototype import plugin_prototype
# start meta
__plugin_name__ = '显示湖id与因子卡片'
__author = 'fffonion'
__version__ = 0.1
__help__ = 'mf显示所有湖及对应卡片，mf 湖id (如mf 10)显示碎片数量'
from cross_platform import *
from xml2dict import XML2Dict
hooks = {}
# extra cmd hook
extra_cmd = {'mf' : 'map_factor', 'map_factor' : 'map_factor'}

def map_factor(plugin_vals):
    def do(*args):
        po = plugin_vals['poster']
        carddb = plugin_vals['carddb']
        r, d = po.post('battle/area')
        resp = XML2Dict().fromstring(d).response
        if(resp.header.error.code != '0'):
            print(du8(resp.header.error.message))
            return
        lakes = resp.body.competition_parts.lake
        if not args[0]:#mf
            print(du8('湖id    湖名称       合成卡片\n' + '-' * 30))
            lakes = sorted(lakes, key = lambda x : int(x.lake_id))
            for l in lakes:
                if l.lake_id == '0':
                    continue
                n = l.title.encode('utf-8')
                l1 = len(n)  # ascii length
                n = du8(n)
                l2 = len(n)  # char count
                print(du8('%-2s%s %s%s%-4s%s' %(
                    l.lake_id,
                    '/活动' if l.event_id != '0' else '     ',
                    n, ' ' * int(13 - l2 - (l1 - l2) / 2),
                    l.master_card_id,
                    carddb[int(l.master_card_id)][0]
                    )))
        else:#mf 20
            lake = [lakes[i] for i in range(len(lakes)) if lakes[i].lake_id == args[0].strip()]
            if not lake:
                print(du8('所选湖尚未开启XD'))
                return
            lake = lake[0]
            print(du8('%s %s%s' % (lake.title, lake.lake_id, lake.complete == '1' and ' 图鉴已开' or '')))
            print('-' * 30)
            for p in lake.parts_list.parts:
                print('%s  ' % p.parts_have, end = '')
                if not int(p.parts_num) % 3:
                    print('\n')
    return do