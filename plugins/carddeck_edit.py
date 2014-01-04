# coding:utf-8
from _prototype import plugin_prototype
import sys
import os
import re
from cross_platform import *
# start meta
__plugin_name__ = 'scratch carddeck from REAL client'
__author = 'fffonion'
__version__ = 0.1
hooks = {}
extra_cmd = {'scratch_carddeck':'scratch_carddeck', 'scc':'scratch_carddeck','check_debug':'check_debug','cd':'check_debug'}
# end meta

def iter_printer(l, sep = '\n'):
    cnt = 1
    str = ''
    for e in l:
        str += '%d.%-10s%s' % (cnt, e.strip('\n'), (cnt % 3 and '' or sep))
        cnt += 1
    return str.decode('utf-8')

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
        print(du8('注意：你必须使用修改版的odex文件才能截获卡组信息！\n你可以输入check_debug或cd来检查修改是否生效。'))
        #check adb existence, wait for device
        print(du8('=======请将手机连接电脑，别忘了打开USB调试，关闭电脑上的各种助手和豆荚'))
        if os.system('adb wait-for-device')==1:
            print(du8('未能运行adb，请去谷歌/度娘下载之-w-'))
            return False
        #clear buffer
        os.system('adb logcat -c')
        #suppress all but D/CJH
        #btw CJH is...what?
        logcat=os.popen('adb logcat CJH:D *:S')
        print(du8('=======Good!'))
        print(du8('请设置一次卡组，并保存\n你可以按Ctrl+C退出'))
        while(1):
            try:
                line=logcat.readline()
                C=re.findall('([\d|empty]+,[\d|empty]+,[\d|empty]+,[\d|empty]+,[\d|empty]+,[\d|empty]+,'
                              '[\d|empty]+,[\d|empty]+,[\d|empty]+,[\d|empty]+,[\d|empty]+,[\d|empty]+)',line)
                if C!=[]:
                    decks = list_option('carddeck')
                    print(du8('\n选择卡组，输入卡组名以添加新卡组'))
                    print(iter_printer(decks))
                    inp = raw_input("> ")
                    if inp in [str(i) for i in range(1, len(decks) + 1)]:
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

    return do

def check_debug(plugin_vals):
    def do(*args):
        print(du8('等待设备连接'))
        os.system('adb wait-for-device')
        os.system('adb logcat -c')
        print(du8('请在游戏中随意执行一个操作。\n如果一直未能显示测试通过，请到这里查看详细帮助https://github.com/fffonion/MAClient/wiki/carddeck_edit'))
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