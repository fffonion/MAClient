# coding:utf-8
import os, os.path as opath
import sys
from cross_platform import *
from xml2dict import XML2Dict

# start meta
__plugin_name__ = 'MAW自动配卡转换插件'
__author = 'fffonion'
__version__ = 0.11
hooks = {}
extra_cmd = {'mi':'maw_importter', 'cmi':'clear_maw_importted'}

def _set_cfg_val(cf, sec, key, val):
    if not cf.has_section(sec):
        cf.add_section(sec)
    cf.set(sec, key, val)

def _write_cfg(cf, fname):
    f = open(fname, "w")
    cf.write(f)
    f.flush()

def maw_importter(plugin_vals):
    def do(*args):
        logger = plugin_vals['logger']
        cf = plugin_vals['cf']
        cfg_file = args[0] if (args[0] and opath.exists(args[0])) else None
        cfg_file = opath.join(getPATH0, 'config.xml') \
                if (opath.exists(opath.join(getPATH0, 'config.xml'))) \
                else cfg_file
        while not cfg_file:
            cfg_file = raw_inputd('输入配置文件的路径 > ')
            if not cfg_file:
                return
            if opath.exists(cfg_file):
                break
            if opath.exists(opath.join(cfg_file, 'config.xml')):
                cfg_file = opath.join(cfg_file, 'config.xml')
                break
            logger.error('输入的路径"%s"不存在配置文件www' % cfg_file)
            cfg_file = None
        try:
            _t = XML2Dict().fromstring(open(cfg_file).read()).config.card
            decks = _t.battle_fairy
        except:
            logger.error('所选"%s"可能不是maw配置文件，或者格式扭曲了TAT' % cfg_file)
            return
        wake_decks = []
        norm_decks = []
        guild_decks = []
        guild_wake_decks = []
        for d in decks:
            if d.wake == '0':
                d_name = norm_decks
                pref = 'norm'
            elif d.wake == '1':
                d_name = wake_decks
                pref = 'wake'
            elif d.wake == '2':
                d_name = guild_decks
                pref = 'guild'
            else:
                d_name = guild_wake_decks
                pref = 'guild_w'

            d_name.append(
                        (
                            '%s and $.hp%%>=%s and BC>=%s' % (
                            '<=$.lv<='.join(d.fairy_lv.split('-')),
                            d.fairy_hp,
                            d.battle_cost
                            ),
                            '%s%s' % (pref, d.fairy_lv)
                        )
                    )
            _set_cfg_val(cf, 'carddeck', '%s%s' % (pref, d.fairy_lv), d.battle_card.rstrip(',empty'))
        
        def _gen_cond(decks):
            ret = ""
            for d in decks:
                ret += "((%s) and '%s' or " % (d[0], d[1])
            ret += "'min'"
            ret += ')' * len(decks)
            return ret
        cond = '$.IS_WAKE and %s or %s' % (_gen_cond(wake_decks), _gen_cond(norm_decks))
        if guild_decks and guild_wake_decks:
            cond = '$.IS_GUILD and ($.IS_WAKE and %s or %s) or (%s)' % (_gen_cond(guild_wake_decks), _gen_cond(guild_decks), cond)
        _set_cfg_val(cf, 'condition', 'fairy_select_carddeck', cond)
        _set_cfg_val(cf, 'carddeck', 'min', _t.lick_fairy.card)
        if _t.pvp.pvp_card:
            _set_cfg_val(cf, 'carddeck', 'factor', _t.pvp.pvp_card)
        _write_cfg(cf, plugin_vals['configfile'])
        print(du8('已保存%d条卡组条件，以及因子战及舔刀卡组\n你可以通过输入cmi命令清除导入的卡组和条件' % len(decks)))
    return do

def clear_maw_importted(plugin_vals):
    def do(*args):
        cf = plugin_vals['cf']
        for key in cf.options('carddeck'):
            if key[:4] in ['norm', 'wake', 'guil']:
                cf.remove_option('carddeck', key)
        _set_cfg_val(cf, 'condition', 'fairy_select_carddeck', "'min'")
        _write_cfg(cf, plugin_vals['configfile'])
        print(du8('导入的卡组和条件已清除，因子战和舔刀卡组没有清除'))
    return do