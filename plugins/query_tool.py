# coding:utf-8
from _prototype import plugin_prototype
import sys
import re
import os
from cross_platform import *
# start meta
__plugin_name__ = 'query infomation of player'
__author = 'fffonion'
__version__ = 0.34
hooks = {}
extra_cmd = {'q_item':'query_item', 'qi':'query_item', 'q_holo':'query_holo', 'qh':'query_holo', 'qgc':'query_guild_contribution','q_rank':'query_rank','qr':'query_rank'}
# end meta

# query item count
def query_item(plugin_vals):
    def do(*args):
        logger = plugin_vals['logger']
        if 'player' not in plugin_vals or not plugin_vals['player'].item.db:
            logger.error(du8('玩家信息未初始化，请随便执行一个操作再试'))
            return
        print(du8('%-17s%s' % ('物品', '个数')))
        print('-' * 30)
        for (i, [n, j]) in plugin_vals['player'].item.db.items():
            if j > 0:  # has
                # calc utf-8 length
                l1 = len(n)  # ascii length
                n = du8(n)
                l2 = len(n)  # char count
                print(du8('%s%s%s' % (n, ' ' * int(15 - l2 - (l1 - l2) / 2), j)))
    return do

# query holo cards
def query_holo(plugin_vals):
    def do(*args):
        logger = plugin_vals['logger']
        if 'player' not in plugin_vals or not plugin_vals['player'].item.db:
            logger.error(du8('玩家信息未初始化，请随便执行一个操作再试'))
            return
        print(du8('%s' % ('当前拥有以下闪卡')))
        print('-' * 30)
        _player = plugin_vals['player']
        cache = []
        for c in _player.card.cards:
            if c.holography == 1:
                ca = _player.card.db[c.master_card_id]
                cache.append((ca[0], ca[1], c.lv, c.hp, c.power))
        cache = sorted(cache, key = lambda l:(l[1], l[2]))
        print('\n'.join(map(lambda x:du8('[%s] ☆%d Lv%d HP:%d ATK:%d' % x), cache)))
    return do

def query_guild_contribution(plugin_vals):
    def do(*args):
        lines = []
        if plugin_vals['loc'][:2] == 'cn':
            lines += open('events_cn.log').read().split('\n')
        elif plugin_vals['loc'] == 'tw':
            lines += open('events_tw.log').read().split('\n')
        else:
            print(du8('不支持%s的查询'%plugin_vals['loc']))
            return
        if os.path.exists('.IGF.log'):
            lines += open('.IGF.log').read().split('\n')
        pname, total = plugin_vals['player'].item.db[8001]
        cnt = 0
        for l in lines:
            c = re.findall(pname+'\]\:\+(\d+)\(',l)
            if c:
                cnt += int(c[0])
        print(du8('公会贡献: %d/ %s'%(cnt,total or '?')))
    return do

def query_rank(plugin_vals):
    def do(*args):
        logger = plugin_vals['logger']
        loc = plugin_vals['loc']
        if loc[:2] not in ['cn','tw']:
            logger.error('排位查询不支持日服和韩服')
            return
        if loc == 'tw':
            import _query_rank_tw_lib as _lib
            import re
            import urllib
            if PYTHON3:
                import urllib.request as urllib2
                opener = urllib2.build_opener(urllib2.ProxyHandler(urllib.request.getproxies()))
            else:
                import urllib2
                opener = urllib2.build_opener(urllib2.ProxyHandler(urllib.getproxies()))
            _header = _lib.broswer_headers
            _header['cookie'] = plugin_vals['cookie']
            _header['User-Agent'] = plugin_vals['poster'].header['User-Agent']
            _guild_mode = 2 if raw_inputd('查询个人排名(s)(默认)还是公会排名(g)> ') == 'g' else 0
            _goto = raw_inputd('输入要查询的排名开始数，按回车显示自己所在区域> ')
            if (_guild_mode and _lib.query_rev[2] and _lib.query_rev[3]) or \
                (not _guild_mode and _lib.query_rev[0] and _lib.query_rev[1]) or _goto:
                _coll_mode = 1 if raw_inputd('查询收集品排名(c)(默认)还是妖精加权排名(f)> ') != 'f' else 0
            else:
                _coll_mode = (1 if _lib.query_rev[3] else 0) if _guild_mode else \
                            (1 if _lib.query_rev[1] else 0)
            def show_it(content):
                strl = '\n%s\n%s\n' %(_lib.query_title(content),'-'*20)
                for (k, v) in _lib.query_regex[_guild_mode + _coll_mode]:
                    try:
                        strl += '%s %s\n' % (k, v(content))
                    except IndexError:
                        pass
                logger.info(strl)
            if _goto:
                _gurl = _lib.query_goto[_guild_mode + _coll_mode]
                if not _goto.isdigit() or \
                    (int(_goto)>20000 and not _guild_mode) or (int(_goto)>2000 and _guild_mode) or \
                    int(_goto)<=0:
                    logger.error('请输入%d以内0以上的数字' % (2000 if _guild_mode else 20000))
                    return
                x = opener.open(urllib2.Request(_gurl % _goto,headers = _header)).read()
                show_it(x)
            else:
                _rev = _lib.query_rev[_guild_mode + _coll_mode]
                if not _rev:
                    logger.error('版本不存在,，请升级_query_rank_lib为新版本\n或指定排名区域查询')
                    return
                if _lib.now >= _lib.query_lifetime:
                    logger.error('查询库已过期，请升级_query_rank_lib为新版本\n或指定排名区域查询')
                    return
                _url = _lib.query_base % _rev
                x = opener.open(urllib2.Request(_url, headers = _header)).read()
                show_it(x)
                
        else:#cn
            from xml2dict import XML2Dict
            po = plugin_vals['poster']
            po.post('menu/menulist')
            sel_rankid = 0
            to_top = False
            while True:
                resp, ct = po.post('ranking/ranking', postdata='move=%d&ranktype_id=%d&top=%d' % (
                                1 if sel_rankid == 0 else 0, sel_rankid, 1 if to_top else 0))
                ct = XML2Dict().fromstring(ct).response.body.ranking
                ranktype_id = int(ct.ranktype_id)
                allranks = ct.ranktype_list.ranktype
                rank_name = allranks[ranktype_id - 1].title
                try:
                    _user = ct.user_list.user
                except KeyError:
                    logging.warning('暂未列入排行榜，请继续努力ww')
                if not to_top:
                    me = [_i for _i in _user if _i.id == plugin_vals['player'].id][0]
                logger.info(rank_name + 
                            (not to_top and '\n排名:%s 点数:%s\n' % (me.rank, me.battle_event_point) or '\n') + 
                            '可见区域内 Up:%s/%s Down:%s/%s' % (
                                _user[0].rank, _user[0].battle_event_point,
                                _user[-1].rank, _user[-1].battle_event_point)
                            )
                while True:
                    _inp = raw_inputd('\n输入序号查询其他排行:(9.排名至顶 0.退出)\n%s\n> ' % 
                                    ('\n'.join(map(lambda x : '%s.%s' % (x.id, x.title), allranks)))
                                ) or '0'
                    if not _inp.isdigit():
                        continue
                    else:
                        if _inp == '0':
                            return
                        if _inp == '9':
                            to_top = True
                        else:
                            sel_rankid = int(_inp)
                            to_top = False
                        break
                    
    return do