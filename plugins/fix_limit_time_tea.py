# coding:utf-8
from _prototype import plugin_prototype
# start meta
__plugin_name__ = '台服优先嗑限时红绿茶'
__author = 'fffonion'
__version__ = 0.20
hooks = {'ENTER__use_item':1, 'EXIT_red_tea':1, 'EXIT_green_tea':1}
extra_cmd = {}
require_version = 1.70
# end meta
import time
import re
import os, os.path as opath
import maclient_smart
from cross_platform import *

if PYTHON3:
    _split = lambda x, y = ',':list(map(lambda x:x.decode('utf-8'), x.encode(encoding = 'utf-8').split(y.encode('utf-8'))))
else:
    _split = lambda x, y = ',':x.split(y)

class plugin(plugin_prototype):
    def __init__(self):
        self.half_offset = maclient_smart.half_bc_offset_tw
        self.already_inhook = False
        self.last_drink_cnt = 0
        self.MINOR_RED, self.MINOR_GREEN = None, None
        self.PERCENT_RED, self.PERCENT_GREEN = 0, 0
        self._guessed_id = False

    def guess_id(self, item):
        _descr = {}
        if PYTHON3:
            f = open(opath.join(getPATH0, 'db/item.tw.txt'), encoding = 'utf8')
        else:
            f = open(opath.join(getPATH0, 'db/item.tw.txt'))
        for c in f.readlines():
            item_line = _split(c)
            #_descr[int(c[0])] = [c[2], 0]
            itm_id = int(item_line[0])
            if item_line[1].find('密藥') != -1 and item.get_count(itm_id) > 0:
                _ = re.findall('(\d+)%', item_line[2])
                if _ == []:
                    continue
                _percent = int(_[0])
                if item_line[1].find('紅色') != -1 and \
                        (not self.MINOR_RED or _percent < self.PERCENT_RED):
                    self.MINOR_RED = itm_id
                    self.PERCENT_RED = _percent
                if item_line[1].find('綠色') != -1 and \
                        (not self.MINOR_GREEN or _percent < self.PERCENT_GREEN):
                    self.MINOR_GREEN = itm_id
                    self.PERCENT_GREEN = _percent
        self._guessed_id = True

    def ENTER__use_item(self, *args, **kwargs):
        mac = args[0]
        itemid = args[1]
        if mac.loc != 'tw' or self.already_inhook:
            return
        if mac.cfg_auto_choose_red_tea and (\
                int(itemid) == 2 and (100 * mac.player.bc['current'] / mac.player.bc['max']) <  1.35 * self.PERCENT_RED \
                or \
                int(itemid) == 1 and (100 * mac.player.ap['current'] / mac.player.ap['max']) <  1.35 * self.PERCENT_GREEN \
            ):#如果勾选 自动选择红绿茶, 且剩余低于1倍小茶回复量，则嗑全回复
            return
        if not self._guessed_id:
            self.guess_id(mac.player.item)
        self.already_inhook = True
        minor_bc_cnt = 0 if not self.MINOR_RED else mac.player.item.get_count(self.MINOR_RED)#为None时，数量设为0
        minor_ap_cnt = 0 if not self.MINOR_GREEN else mac.player.item.get_count(self.MINOR_GREEN)
        
        if int(itemid) == 2:
            iid= self.MINOR_RED
            cnt = min(100/self.PERCENT_RED, minor_bc_cnt)
        elif int(itemid) == self.half_offset + 2:
            iid= self.MINOR_RED
            cnt = min(50/self.PERCENT_RED, minor_bc_cnt)
        elif int(itemid) == 1:
            iid= self.MINOR_GREEN
            cnt = min(100/self.PERCENT_GREEN, minor_ap_cnt)
        elif int(itemid) == self.half_offset + 1:
            iid= self.MINOR_GREEN
            cnt = min(50/self.PERCENT_GREEN, minor_ap_cnt)
        #adjust count
        if iid == self.MINOR_RED:
            cnt = min(int((100 - 100 * mac.player.bc['current'] / mac.player.bc['max']) / self.PERCENT_RED), cnt)
        else:
            cnt = min(int((100 - 100 * mac.player.ap['current'] / mac.player.ap['max']) / self.PERCENT_GREEN), cnt)
        if cnt == 0:
            self.already_inhook = False
            #args = (mac, 0)#不喝任何茶
            return
        self.last_drink_cnt = cnt
        mac.logger.info('将使用%d瓶"%s"' % (cnt, mac.player.item.get_name(iid)))
        for i in range(cnt - 1):
            try:
                mac._use_item(iid)
                time.sleep(1.414)
            except KeyboardInterrupt:
                break
            except ValueError:#ctrl+c caused incomplete read
                break
        args = (mac, iid)
        self.already_inhook = False
        return args, kwargs

    # 修正已喝数量
    def EXIT_red_tea(self, *args, **kwargs):
        if self.last_drink_cnt > 0:
            old = float(args[0]._read_config('tactic', 'auto_red_tea') or '0')
            res = old + 1 - self.last_drink_cnt * self.PERCENT_RED / 100.0
            args[0]._write_config('tactic', 'auto_red_tea', str(0 if res < 0 else res))
            self.last_drink_cnt = 0

    def EXIT_green_tea(self, *args, **kwargs):
        if self.last_drink_cnt > 0:
            old = float(args[0]._read_config('tactic', 'auto_green_tea') or '0')
            res = old + 1 - self.last_drink_cnt * self.PERCENT_GREEN / 100.0
            args[0]._write_config('tactic', 'auto_green_tea', str(0 if res < 0 else res))
            self.last_drink_cnt = 0


