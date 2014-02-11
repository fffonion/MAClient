# coding:utf-8
from _prototype import plugin_prototype
from cross_platform import *
import time
# start meta
__plugin_name__ = '狼娘无限舔公会妖'
__author = 'fffonion'
__version__ = 0.4
__tip__ = '插件已开启，如需关闭请移除plugins下的infinite_guild_fairy'
hooks = {'EXIT__fairy_battle':10}
# extra cmd hook
extra_cmd = {'rbl':'rollback_log'}
# end meta
class plugin(plugin_prototype):
    def __init__(self):
        self.__name__ = __plugin_name__
        self.mac_instance = None
        self._ori_logfile = None

    def fairy_floor(self,fairy):
        paramfl = 'check=1&race_type=%s&serial_id=%s&user_id=%s' % (
            fairy.race_type, fairy.serial_id, fairy.discoverer_id)
        resp, ct = self.mac_instance._dopost('exploration/fairy_floor', postdata = paramfl)
        if resp['error']:
            return None
        else:
            return ct.body.fairy_floor.explore.fairy

    def _rollback_log(self):
        self.logger.logfile.flush()
        self.logger.logfile.close()
        self.logger.logfile = self._ori_logfile
        self._ori_logfile = None

    def EXIT__fairy_battle(self, *args, **kwargs):
        self.logger = args[0].logger
        if not self._ori_logfile:#不记录
            self.logger.logfile.flush()
            self._ori_logfile = self.logger.logfile
            self.logger.setlogfile('.IGF.log') 
        fairy=args[1]
        if fairy.race_type in ['11', '12'] and fairy.time_limit != '0':
            print(du8("公会妖精！"))
            self.mac_instance = args[0]
            self.mac_instance.lastfairytime=0
            fairy=self.fairy_floor(fairy)
            if fairy.hp == '0' or fairy.time_limit == '0':
                self._rollback_log()
                return
            if self.mac_instance.player.bc['current']>=2:
                time.sleep(1)
                self.mac_instance._fairy_battle(fairy, carddeck = 'min', bt_type = 0)#0 -> EXPLORE_BATTLE 不用重新fairy_floor
            else:
                if not self.mac_instance.red_tea(silent = True):
                    _t = self.mac_instance.player.bc['interval_time'] * 2
                    print(du8("BC<2，%.1f分钟后再战ww" % (_t/60.0)))
                    time.sleep(_t)
                self.mac_instance._fairy_battle(fairy, carddeck = 'min', bt_type = 0)
        else:
            self._rollback_log()

def rollback_log(plugin_vals):
    def do(*args):
        plugin_vals['logger'].setlogfile('events_%s.log'%plugin_vals['loc'])
    return do
