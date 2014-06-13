# coding:utf-8
from _prototype import plugin_prototype
# start meta
__plugin_name__ = '台服优先嗑限时红绿茶'
__author = 'fffonion'
__version__ = 0.19
hooks = {'ENTER__use_item':1, 'EXIT_red_tea':1, 'EXIT_green_tea':1}
extra_cmd = {}
require_version = 1.70
# end meta
import time
import maclient_smart
MINOR_RED, MINOR_GREEN = None, None
PERCENT = 7
class plugin(plugin_prototype):
    def __init__(self):
        self.half_offset = maclient_smart.half_bc_offset_tw
        self.already_inhook = False
        self.last_drink_cnt = 0

    def guess_id(self, item):
        global MINOR_RED
        global MINOR_GREEN
        for itm_id in item.db.keys()[::-1]:
            if item.get_name(itm_id).find('梅林的') != -1 and item.get_count(itm_id):#>0
                if item.get_name(itm_id).find('紅色') != -1 and not MINOR_RED:
                    MINOR_RED = itm_id
                if item.get_name(itm_id).find('綠色') != -1 and not MINOR_GREEN:
                    MINOR_GREEN = itm_id

    def ENTER__use_item(self, *args, **kwargs):
        mac = args[0]
        itemid = args[1]
        if mac.loc != 'tw' or self.already_inhook:
            return
        if mac.cfg_auto_choose_red_tea and (\
                int(itemid) == 2 and (100 * mac.player.bc['current'] / mac.player.bc['max']) <  1.35 * PERCENT \
                or \
                int(itemid) == 1 and (100 * mac.player.ap['current'] / mac.player.ap['max']) <  1.35 * PERCENT \
            ):#如果勾选 自动选择红绿茶, 且剩余低于1倍小茶回复量，则嗑全回复
            return
        if not MINOR_RED or not MINOR_GREEN:
            self.guess_id(mac.player.item)
        self.already_inhook = True
        minor_bc_cnt = 0 if not MINOR_RED else mac.player.item.get_count(MINOR_RED)
        minor_ap_cnt = 0 if not MINOR_GREEN else mac.player.item.get_count(MINOR_GREEN)
        
        if int(itemid) == 2:
            iid= MINOR_RED
            cnt = min(100/PERCENT, minor_bc_cnt)
        elif int(itemid) == self.half_offset + 2:
            iid= MINOR_RED
            cnt = min(50/PERCENT, minor_bc_cnt)
        elif int(itemid) == 1:
            iid= MINOR_GREEN
            cnt = min(100/PERCENT, minor_ap_cnt)
        elif int(itemid) == self.half_offset + 1:
            iid= MINOR_GREEN
            cnt = min(50/PERCENT, minor_ap_cnt)
        #adjust count
        if iid == MINOR_RED:
            cnt = min(int((100 - 100 * mac.player.bc['current'] / mac.player.bc['max']) / PERCENT), cnt)
        else:
            cnt = min(int((100 - 100 * mac.player.ap['current'] / mac.player.ap['max']) / PERCENT), cnt)
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
            res = old + 1 - self.last_drink_cnt * PERCENT / 100.0
            args[0]._write_config('tactic', 'auto_red_tea', str(0 if res < 0 else res))
            self.last_drink_cnt = 0

    def EXIT_green_tea(self, *args, **kwargs):
        if self.last_drink_cnt > 0:
            old = float(args[0]._read_config('tactic', 'auto_green_tea') or '0')
            res = old + 1 - self.last_drink_cnt * PERCENT / 100.0
            args[0]._write_config('tactic', 'auto_green_tea', str(0 if res < 0 else res))
            self.last_drink_cnt = 0


