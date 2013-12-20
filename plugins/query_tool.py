# coding:utf-8
from _prototype import plugin_prototype
import sys
from cross_platform import *
# start meta
__plugin_name__ = 'query infomation of player'
__author = 'fffonion'
__version__ = 0.1
hooks = {}
extra_cmd = {'query_item':'query_item', 'qi':'query_item', 'query_holo':'query_holo', 'qh':'query_holo'}
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
