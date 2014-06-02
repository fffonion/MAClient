# coding:utf-8
from _prototype import plugin_prototype
from cross_platform import *
# start meta
__plugin_name__ = '日服自动点赞'
__author = 'fffonion'
__version__ = 0.2
hooks = {'EXIT_fairy_select':1}
extra_cmd = {}
# end meta
class plugin(plugin_prototype):
    def __init__(self):
        self._given_good_list = []

    def EXIT_fairy_select(self, *args, **kwargs):
        #点赞用 参考自MAWalker
        mac = args[0]
        if mac.loc != 'jp':
            return
        fairies = kwargs['pop_extras']('fairy_event')
        if not fairies or len(fairies) == 0:
            return
        mac.logger.info('找到%d个可赞的妹纸啦...' % len(fairies))
        for f in fairies:
            resp, ct = mac._dopost('private_fairy/private_fairy_history',
                        postdata = 'serial_id=%s&user_id=%s' % (f.fairy.serial_id, f.fairy.discoverer_id),
                        )
            if resp['error']:
                continue
            buddies = mac.tolist(ct.body.fairy_history.attacker_history.attacker)
            buddy_str = ','.join(map(lambda x:x.user_id, [b for b in buddies if b.user_id != mac.player.id]))
            if not buddy_str:
                pass#continue
            resp, ct = mac._dopost('private_fairy/private_fairy_battle_good',
                        postdata = 'dialog=1&serial_id=%s&user_id=%s' % (f.fairy.serial_id, buddy_str),
                        )
            if resp['error']:
                continue
            