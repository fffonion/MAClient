# coding:utf-8
import re
import httplib2
import time
import random
from _prototype import plugin_prototype
import maclient_network
from cross_platform import *

# start meta
__plugin_name__ = '统计11连掉率'
__author = 'fffonion'
__version__ = 0.1
hooks = {}
extra_cmd = {'gs':'gacha_stats'}
# end meta
# generate weburl
weburl = dict(maclient_network.serv)
for k in weburl:
    weburl[k] = weburl[k].replace('app/', 'web/?%s')

servers = ['static.sdg-china.com' ,'ma.webpatch.sdg-china.com', 'game.ma.mobimon.com.tw', 'web.million-arthurs.com', 'ma.actoz.com']
# other stuffs
headers = {'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'X-Requested-With': 'com.square_enix.million_tw',
    'User-Agent': '',
    'Accept-Language': 'zh-CN, en-US',
    'Accept-Charset': 'utf-8, iso-8859-1, utf-16, *;q=0.7',
    'Referer':'http://game.ma.mobimon.com.tw:10001/connect/web/mb_itemstorebuy_makesure?id=2&quantity=11'}
    # 'Accept-Encoding':'gzip,deflate'}

cached = {}
def _query_name(db, name):
    if name in cached:
        return cached[name]
    for mid in db:
        if db[mid][0] == name:
            cached[name] = db[mid][1]
            return db[mid][1]

ht = httplib2.Http(proxy_info = httplib2.ProxyInfo(httplib2.socks.PROXY_TYPE_HTTP_NO_TUNNEL, "127.0.0.1", 23333))
def gacha_stats(plugin_vals):
    def do(*args):
        carddb = plugin_vals['player'].card.db
        holo_cnt = 0
        total_cnt = 0
        star_cnt = [0, 0, 0, 2480,2659,314,47]
        holo_cnt = [0, 0, 0, 25,25,25,0]
        rarity = ['', '' ,'' ,'R+ ', 'SR', 'SR+', 'MR']
        rnd = int(args[0].rstrip()) if (len(args) > 0 and args[0].rstrip().isdigit()) else 10
        headers['cookie'] = plugin_vals['cookie']
        headers['User-Agent'] = plugin_vals['poster'].header['User-Agent']
        for i in range(rnd):
            htmldoc = ht.request('http://game.ma.mobimon.com.tw:10001/connect/web/mb_itemstorebuy?id=2&quantity=50', 
                headers = headers)[1]
            cards = map(lambda x:x.decode('utf-8'), 
                    re.findall('<div class="blanklist card_window">.*?<p>(.*?) x \d.*?</div>', htmldoc, re.DOTALL)
                )
            total_cnt += len(cards)
            f = open(r'z:/result.txt','a', False)
            for card in cards:
                is_holo = False
                if card.find('(閃)') != -1:
                    card = card.replace('(閃)', '')
                    is_holo = True
                st = _query_name(carddb, card)
                if is_holo:
                    holo_cnt[st - 1] += 1
                star_cnt[st - 1] += 1
                f.write('☆%d %s%s %s%s\r\n' % (_query_name(carddb, card),
                                            'B' if 'BLACK' in card else ' ',
                                            rarity[st - 1],
                                            card, '(閃)' if is_holo else '')) 
            print('Round %d %d(%s) HOLO:%d(%s) ' % (i + 1, 
                                        total_cnt, ','.join(map(lambda x:str(x), star_cnt[3:])), 
                                        sum(holo_cnt[3:]), ','.join(map(lambda x:str(x), holo_cnt[3:])),
                                        ))
            f.write('\r\n')
            f.close()
            time.sleep(random.randrange(3, 10) * 0.618)
    return do



