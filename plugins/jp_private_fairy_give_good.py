# coding:utf-8
from _prototype import plugin_prototype
from cross_platform import *
# start meta
__plugin_name__ = '日服自动点赞'
__author = 'fffonion'
__version__ = 0.31
hooks = {'EXIT_fairy_select':1}
extra_cmd = {'good':'set_give_good'}
# end meta

def _write(cf, sec, key, val):
    if not cf.has_section(sec):
        cf.add_section(sec)
    cf.set(sec, key, val)

def set_give_good(plugin_vals):
    '''
    命令：
    good 启用
    good 1 启用
    good 0 禁用
    good False 禁用
        ...
    '''
    def do(*args):
        if args[0].strip() in ['0', 'False', 'false']:
            _write(plugin_vals['cf'], 'plugin', 'jp_private_fairy_good_disabled', 1)
            plugin_vals['logger'].info('点赞已禁用')
        else:
            _write(plugin_vals['cf'], 'plugin', 'jp_private_fairy_good_disabled', 0)
            plugin_vals['logger'].info('点赞已启用')
    return do

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
        if mac._read_config('plugin', 'jp_private_fairy_good_disabled') == '1':
            mac.logger.warning('点赞已被禁用啦...')
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
            