# coding:utf-8
from _prototype import plugin_prototype
import re
from cross_platform import *
# start meta
__plugin_name__ = '手动添加倍卡信息'
__author = 'fffonion'
__version__ = 0.1
hooks = {}
extra_cmd = {'add_multi':'add_multi', 'am':'add_multi'}
# end meta

def add_multi(plugin_vals):
    def do(*args):
        carddb = plugin_vals['carddb']
        loc = plugin_vals['loc'][:2]
        print(du8('自定义倍卡添加工具(*￣︶￣)y 按回车退出\n'))
        cached = []
        while True:
            inp = raw_inputd('请输入卡片的名称/部分名称/id > ')
            found = False
            if not inp:
                break
            elif not inp.isdigit():#name
                for c in carddb:
                    if re.search(inp, carddb[c][0]):
                        found = True
                        break
                inp = c
            else:
                inp = int(inp)
                found = inp in carddb
            if not found:
                print(du8('卡片不存在'))
                continue
            else:
                while True:
                    multi = raw_inputd('请输入倍率 > ')
                    if multi.isdigit() or not multi:
                        break
            cached.append((inp, multi))
        if not cached:
            return
        preserve_old = raw_inputd('保留已存在的倍卡数据?(y/n)') == 'y'
        _f = opath.join(getPATH0, 'db/card.multi.txt')
        if PYTHON3:
            kw = {'encoding' : 'utf-8'}
        else:
            kw = {}
        lines = open(_f, **kw).readlines()
        wrote = False
        with open(_f, 'w', **kw) as f:
            for line in lines:
                if line.startswith(loc):
                    wrote = True
                    line = ((line + ';') if preserve_old else (loc + '=')) + \
                        ';'.join(map(lambda x:'%d,%s' % (x[0], x[1]), cached))
                f.write(line)
            if not wrote:
                f.write(loc + '=' + ';'.join(map(lambda x:'%d,%s' % (x[0], x[1]), cached)))
        print(du8('写入了%d条倍卡数据，重新启动MAClient以应用修改' % len(cached)))
    return do