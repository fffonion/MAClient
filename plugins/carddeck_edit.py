# coding:utf-8
from _prototype import plugin_prototype
import sys
import os
from subprocess import Popen, PIPE
import re
from cross_platform import *
from xml2dict import XML2Dict
# start meta
__plugin_name__ = 'scratch carddeck from REAL client'
__author = 'fffonion'
__version__ = 0.4
hooks = {}
extra_cmd = {'scratch_carddeck':'scratch_carddeck', 'scc':'scratch_carddeck','check_debug':'check_debug','cd':'check_debug',
'read_decks':'read_decks','rd':'read_decks'}
# end meta
def tolist(obj):
    if not isinstance(obj, list):
        return [obj]
    else:
        return obj

def iter_printer(l, sep = '\n'):
    cnt = 1
    str = ''
    for e in l:
        str += '%d.%-10s%s' % (cnt, e.strip('\n'), (cnt % 3 and '' or sep))
        cnt += 1
    return str.decode('utf-8')

def read_decks(plugin_vals):
    def do(*args):
        if plugin_vals['loc'] == 'jp':
            get=lambda x, y:XML2Dict().fromstring(x).response.body.roundtable_edit.deck[y - 1].deck_cards
        else:
            get=lambda x, y:XML2Dict().fromstring(x).response.body.roundtable_edit.deck_cards
        poster=plugin_vals['poster']
        pcard=plugin_vals['player'].card
        cf=plugin_vals['cf']
        def write_config(sec, key, val):
            if not cf.has_section(sec):
                cf.add_section(sec)
            cf.set(sec, key, val)
            f = open(plugin_vals['configfile'], "w")
            cf.write(f)
            f.flush()
        list_option=cf.options
        _jp_cache = None
        for i in (plugin_vals['loc'] == 'jp' and range(1,5,1) or range(1,4,1)):
            if i == 4:
                print(du8('推荐卡组:'))
            else:
                print(du8('卡组%d:' % i))
            if plugin_vals['loc'] == 'jp':
                if not _jp_cache:
                    _jp_cache = poster.post('roundtable/edit', postdata = 'move=1')[1]
                _data = _jp_cache
            else:
                _data = poster.post('roundtable/edit', postdata = 'move=1%s'%(i>1 and '&deck_id=%s'%i or ''))[1]
            try:
                C=get(_data, i).rstrip(',empty').split(',')
                assert(C != [''])
            except AssertionError:
                print(du8('卡组为空，跳过ww'))
                continue
            # except:
            #     print(du8('读取卡组失败，请输入rl重新登录'))
            #     return
            CL=tolist(C)
            print(du8('\n'.join(['|'.join(map(
                    lambda x:'   %-12s' % pcard.db[pcard.sid(x).master_card_id][0],
                    C[i:min(i + 3, len(CL))]
                 )) for i in range(0, len(CL), 3)])).encode(CODEPAGE or 'utf-8', 'replace'))
            decks = list_option('carddeck')
            print(du8('\n选择卡组，输入卡组名以添加新卡组，按回车跳过'))
            print(iter_printer(decks))
            inp = raw_input("> ")
            if inp == "":
                continue
            elif inp in [str(i) for i in range(1, len(decks) + 1)]:
                name = decks[int(inp) - 1]
            else:
                name = inp
            write_config('carddeck', name, ','.join(C))
            print(du8('保存到了%s' % name))
        #poster.post('roundtable/edit', postdata = 'move=1&deck_id=1')
    return do

def scratch_carddeck(plugin_vals):
    def do(*args):
        cf=plugin_vals['cf']
        list_option=cf.options
        def write_config(sec, key, val):
            if not cf.has_section(sec):
                cf.add_section(sec)
            cf.set(sec, key, val)
            f = open(plugin_vals['configfile'], "w")
            cf.write(f)
            f.flush()
        print(du8('注意：你必须使用修改版的odex文件才能截获卡组信息！\n你可以输入check_debug或cd来检查修改是否生效。\n你也可以使用更简单的read_decks来读取卡组'))
        #check adb existence, wait for device
        print(du8('=======请将手机连接电脑，别忘了打开USB调试，关闭电脑上的各种助手和豆荚'))
        if os.system('adb wait-for-device')==1:
            print(du8('未能运行adb，请去谷歌/度娘下载之-w-'))
            return False
        #clear buffer
        os.system('adb logcat -c')
        #suppress all but D/CJH
        #btw CJH is...what?
        logcat=Popen('adb logcat CJH:D *:S', stdout = PIPE)
        print(du8('=======Good!'))
        print(du8('请设置一次卡组，并保存\n你可以按Ctrl+C退出'))
        while(1):
            try:
                line = logcat.stdout.readline()
                if not line:
                    break
                C=re.findall('([\d|empty]+,[\d|empty]+,[\d|empty]+,[\d|empty]+,[\d|empty]+,[\d|empty]+,'
                              '[\d|empty]+,[\d|empty]+,[\d|empty]+,[\d|empty]+,[\d|empty]+,[\d|empty]+)',line)
                if C!=[]:
                    decks = list_option('carddeck')
                    print(du8('\n选择卡组，输入卡组名以添加新卡组'))
                    print(iter_printer(decks))
                    inp = raw_input("> ")
                    if inp == "":
                        continue
                    elif inp in [str(i) for i in range(1, len(decks) + 1)]:
                        name = decks[int(inp) - 1]
                    else:
                        name = inp
                    write_config('carddeck', name, C[0].rstrip(',empty'))
                    print(du8('保存到了%s' % name))
                else:
                    continue
            except KeyboardInterrupt:
                break
            print(du8('请设置一次卡组，并保存\n你可以按Ctrl+C退出'))
        os.system('adb kill-server')
    return do

def check_debug(plugin_vals):
    def do(*args):
        print(du8('等待设备连接'))
        os.system('adb wait-for-device')
        os.system('adb logcat -c')
        print(du8('请在游戏中随意执行一个操作。\n如果一直未能显示测试通过，请到这里查看详细帮助\nhttps://github.com/fffonion/MAClient/wiki/carddeck_edit'))
        logcat=os.popen('adb logcat CJH:D *:S')
        while(1):
            try:
                line=logcat.readline()
            except KeyboardInterrupt:
                break
            if line.startswith('D/CJH'):
                print(du8('测试通过！现在你可以输入scratch_carddeck或scc来抓取卡组了\n请按Ctrl+C退出'))
                return
    return do