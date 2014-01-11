# coding:utf-8
from _prototype import plugin_prototype
from cross_platform import *
import time
# start meta
__plugin_name__ = '狼娘无限舔公会妖'
__author = 'fffonion'
__version__ = 0.3
__tip__ = '插件已开启，如需关闭请移除plugins下的infinite_guild_fairy'
hooks = {'EXIT__fairy_battle':10}
# extra cmd hook
extra_cmd = {}
# end meta
class plugin(plugin_prototype):
    def __init__(self):
        self.__name__ = __plugin_name__
        self.mac_instance = None
        self._ori_logfile = ''

    def fairy_floor(self,fairy):
        paramfl = 'check=1&race_type=%s&serial_id=%s&user_id=%s' % (
            fairy.race_type, fairy.serial_id, fairy.discoverer_id)
        resp, ct = self.mac_instance._dopost('exploration/fairy_floor', postdata = paramfl)
        if resp['error']:
            return None
        else:
            return ct.body.fairy_floor.explore.fairy

    def EXIT__fairy_battle(self, *args, **kwargs):
        self.logger = args[0].logger
        if not self._ori_logfile:#不记录
            self._ori_logfile = self.logger.logfile
            self.logger.setlogfile('.IGF.log') 
        fairy=args[1]
        if fairy.race_type == '12' and fairy.time_limit != '0':
            print(du8("公会妖精！"))
            self.mac_instance = args[0]
            self.mac_instance.lastfairytime=0
            if self.mac_instance.player.bc['current']>=2:
                time.sleep(5)
                fairy=self.fairy_floor(fairy)
                if fairy.hp == '0' or fairy.time_limit == '0':
                    #rollback
                    self.logger.setlogfile(self._ori_logfile)
                    self._ori_logfile = ''
                    return
                self.mac_instance._fairy_battle(fairy, kwargs)
            else:
                if not self.mac_instance.red_tea(silent = True):
                    print(du8("BC<2，两分钟后再战ww"))
                    time.sleep(120)
                self.mac_instance._fairy_battle(fairy, kwargs)

            
