# coding:utf-8
from _prototype import plugin_prototype
from cross_platform import *
# start meta
__plugin_name__ = '领礼物盒里x星以上卡片'
__author = 'fffonion'
__version__ = 0.2
__tip__ = '如输入 rb !5 领取5星及以上卡片'
hooks = {'ENTER_reward_box':1}
extra_cmd = {}
# end meta
class plugin(plugin_prototype):
    def ENTER_reward_box(self, *args, **kwargs):
        if len(args) > 1:
            rw_type = args[1]
        elif 'rw_type' in kwargs:
            rw_type = kwargs.pop('rw_type')
        else:
            return
        if not rw_type.startswith('!'):
            return
        _star = rw_type[1:]
        if not _star.rstrip('>').rstrip('<').isdigit():
            return
        star = int(_star.rstrip('>').rstrip('<'))
        mac = args[0]
        print(du8('将领取所有☆%d及以上卡片' % star))
        regexp = ''
        for c in mac.carddb:
            if mac.carddb[c][1] >= star:
                # +商城快遞 是为了防止 炎夏型菲 匹配 炎夏型菲米娜
                # 礼物标题被合并成类似 行樂型菲爾丹商城快遞行樂型菲爾丹
                regexp += mac.carddb[c][0].decode('utf-8') + '商城快遞|' 
        regexp = regexp.rstrip('|')
        if not regexp:
            regexp = 'NOTHING-NOTHING-NOTHING'# make regexp not match anything
        else:
            if rw_type[-1] == '>':
                regexp += '>'
            if rw_type[-1] == '<':
                regexp += '<'
        args = self.tuple_assign(args, 1, regexp)
        return args, kwargs