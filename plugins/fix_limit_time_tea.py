# coding:utf-8
from _prototype import plugin_prototype
# start meta
__plugin_name__ = '台服优先嗑限时红绿茶'
__author = 'fffonion'
__version__ = 0.15
hooks = {'ENTER__use_item':1}
extra_cmd = {}
require_version = 1.68
# end meta
import time
import maclient_smart
MINOR_RED, MINOR_GREEN = 5010, 5009
class plugin(plugin_prototype):
    def __init__(self):
        self.half_offset = maclient_smart.half_bc_offset_tw
        self.already_inhook = False
        pass

    def ENTER__use_item(self, *args, **kwargs):
        mac = args[0]
        if mac.loc != 'tw' or self.already_inhook:
            return
        self.already_inhook = True
        itemid = args[1]
        minor_bc_cnt = mac.player.item.get_count(MINOR_RED)
        minor_ap_cnt = mac.player.item.get_count(MINOR_GREEN)
        #10瓶秘药顶50%, 20瓶顶100%
        if int(itemid) == 2:
            iid= MINOR_RED
            cnt = min(20, minor_bc_cnt)
        elif int(itemid) == self.half_offset + 2:
            iid= MINOR_RED
            cnt = min(10, minor_bc_cnt)
        elif int(itemid) == 1:
            iid= MINOR_GREEN
            cnt = min(20, minor_ap_cnt)
        elif int(itemid) == self.half_offset + 1:
            iid= MINOR_GREEN
            cnt = min(10, minor_ap_cnt)
        if cnt == 0:
            self.already_inhook = False
            return
        mac.logger.info('将使用%d瓶"%s"' % (cnt, mac.player.item.get_name(iid)))
        args = (mac, iid)
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