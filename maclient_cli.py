#!/usr/bin/env python
# coding:utf-8
#qpy:console
# maclient command line interface
# Contributor:
#      fffonion        <fffonion@gmail.com>
from __future__ import print_function
import sys
# for ironpython build
import zipimport
sys.path.append('python27.zip')
import time
import socket
# import httplib2
import os
import os.path as opath
import threading
import traceback
import maclient
import maclient_proxy
import maclient_logging
from cross_platform import *
# look out for ironpython

# def iter_printer(l, sep = '\n'):
#     cnt = 1
#     str = ''
#     for e in l:
#         str += '%d.%-10s%s' % (cnt, e.strip('\n'), (cnt % 3 and '' or sep))
#         cnt += 1
#     return str.decode('utf-8')

def getTerminalSize():
    # http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
    if os.name == 'nt':
        if NICE_TERM:
            return 100,80
        env = os.environ
        dres = None
        try:
            from ctypes import windll, create_string_buffer
            h = windll.kernel32.GetStdHandle(-12)
            csbi = create_string_buffer(22)
            res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
        except:
            return None
        if res:
            import struct
            (bufx, bufy, curx, cury, wattr,
             left, top, right, bottom, maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
            sizex = right - left + 1
            sizey = bottom - top + 1
            return sizex, sizey
        else:
            return 120, 80
    else:
        try:
            x, y = os.popen('stty size', 'r').read().split()
        except ValueError:
            x, y = 120, 80
        return int(y), int(x)

class srv(threading.Thread):
    def __init__(self, server):
        self.server = server
        threading.Thread.__init__(self)
    def run(self):
        self.server.serve_forever()


def read_proxy():
    serverport = 23300
    server_address = ("", serverport)
    hdl = maclient_proxy.Handler
    server = maclient_proxy.ThreadingHTTPServer(server_address, hdl)
    # Random Target Proxy Server
    #if work == 0:
    print(du8('请将设备的代理设置为 %s:%s 然后随便进行一次操作' % (socket.gethostbyname(socket.gethostname()),serverport)))
    # elif work == 1:
    #     print(du8('请将设备的代理设置为 本机ip:%s 然后设定一次卡组\n除了这种办法，你还可以直接在config.ini中输入所需卡片的卡片id，如小狼女: 124\n可以在db/card.tw.txt或db/card.tw.txt中查找' % (serverport)))
    srver = srv(server)
    srver.setDaemon(True)
    srver.start()
    while True:
        if os.path.exists('.session'):
            sessionid = open('.session', 'r').read()
            print('found sessionid :%s' % sessionid)
            srver.join(1)
            os.remove('.session')
            return sessionid
        # elif work == 1 and os.path.exists('.carddeck'):
        #     carddeck = open('.carddeck', 'r').read()
        #     print('found carddeck change')
        #     srver.join(1)
        #     os.remove('.carddeck')
        #     return carddeck
        time.sleep(1)

def release_socket(socket_pool):
    for s in socket_pool:
        socket_pool[s].close()
    socket_pool = {}

def bug_reporter(traceback, comment = None, poster = None):
    import urllib
    import httplib2
    cfg = ''
    if maclient1:
        for k in maclient1.__dict__:
            if k.startswith('cfg_'):
                cfg += '%s = %s\n' % (k[4:], maclient1.__dict__[k])
        for k in ['fairy_select', 'explore_area', 'explore_floor', 'select_card_to_sell', 'fairy_select_carddeck', 'factor']:
            cfg += '\n%s = %s' % (k, maclient1._read_config('condition',k))
    cmt = urllib.quote(('MAClient %s Debug Report\n\n\n'
                        '############## Comment #############\n'
                        '%s\n\n'
                        '########## Traceback Info ##########\n'
                        '%s\n\n'
                        '########## Configurations ##########\n'
                        '%s' % (
            maclient.__version__,
            comment,
            traceback,
            cfg
        )).encode('utf8'))
    poster = urllib.quote(poster if poster else 'MAClient User')
    try:
        h = httplib2.Http()
        h.follow_redirects = False
        r, c = h.request('http://pastebin.mozilla.org',
            method = 'POST',
            body = 'parent_pid=&format=Python&code2=%s&poster=%s&paste=Send&expiry=m' % (cmt, poster),
            headers = {'Content-Type': 'application/x-www-form-urlencoded',
                      'User-Agent':'MAClient%s' % maclient.__version__})
        return r['location'][28:]#return numbers
    except:
        return None

logging = maclient_logging.Logging('logging')
maclient1 = None
def main():
    global maclient1
    if not PYTHON3:
        reload(sys)
        sys.setdefaultencoding('utf-8')
    # ht=httplib2.Http(timeout=30)
    print(du8('%s%sv%s%s' % ('=' * int((getTerminalSize()[0] - 5 - 18) / 2), '丧心病狂的MA客户端', maclient.__version__, '=' * int((getTerminalSize()[0] - 5 - 18) / 2))))
    if ANDROID:
        os.chdir(os.environ.get('ANDROID_ARGUMENT'))
    if len(sys.argv) > 2:
        maclient1 = maclient.MAClient(configfile = sys.argv[1], savesession = True)
        # auth()
        maclient1.login()
        arg = ' '.join(sys.argv[2:])
        pos = arg.find('t:')
        if pos != -1:
            maclient1.tasker(taskname = arg[pos + 2:])
        else:
            maclient1.tasker(cmd = arg)
    else:
        if len(sys.argv) == 2:
            maclient1 = maclient.MAClient(configfile = sys.argv[1], savesession = True)
        else:
            try:
                import androidhelper # android!
            except ImportError:
                maclient1 = maclient.MAClient(savesession = True)
            else:
                if os.path.exists('config.ini'):
                    maclient1 = maclient.MAClient(savesession = True)
                else:
                    droid = androidhelper.Android()
                    line = droid.dialogGetInput("MAClient", "请输入配置文件名", "")
                    if not line.result:
                        sys.exit(0)
                    else:
                        maclient1 = maclient.MAClient(configfile = line.result, savesession = True)

        # 进入游戏
        # maclient1._dopost('post_token',postdata=ma.encode_param('S=nosessionid&login_id=%s&password=%s&app=and&token=BubYIgiyDYTFUifydHIoIOGBiujgRzrEFUIbIKOHniHIoihoiHasbdhasbdUIUBujhbjhjBJKJBb'%(username,password)),usecookie=True,extraheader={'Cookie2': '$Version=1'})
        # 登陆
        #server = maclient1._read_config('remote', 'maCServer') or 'http://mac.yooooo.us'
        # auth()
        mode = ['普通', '同时在线']
        mod = 0
        history = []
        while True:
            print(du8('This is a kingdom\'s junction. Tell me your select.【Mode:%s Server:%s】\n\n1.进入游戏\t\tas.自动配卡\n2.切换模式->%s\te.刷秘境\n3.编辑卡组\t\tfyb.刷妖精\n4.编辑配置\t\tfcb.因子战\n5.更新数据库\t\tf.好友相关\n6.退出\t\t\th.命令列表%s' % (
                mode[mod],
                maclient1._read_config('system', 'server'),
                mode[(mod + 1) % 2],
                maclient1.plugin.extra_cmd and '(+%d)' % len(maclient1.plugin.extra_cmd) or '')))
            print('Select> ', end = '')
            if PYTHON3:
                ch = input()
            else:
                ch = sys.stdin.readline().rstrip('\n').decode(locale.getdefaultlocale()[1] or 'utf-8')#.encode('utf-8')
            try:
                print(' \b')
            except KeyboardInterrupt:
                maclient1._exit()
            #history
            if ch.startswith('!'):
                if ch == '!!':
                    ch = '!1'
                if(int(ch[1:])>len(history)):
                    maclient1.logger.warning('历史越界 idx:%s len:%d'%(ch[1:],len(history)))
                    continue
                else:
                    ch = history[-int(ch[1:])]
                    print(du8(ch))
            else:
                if not history or history[-1] != ch:
                    history.append(ch)
                    if len(history)>10:
                        history = history[-10:]
            if ch == '1' or ch == '':
                try:
                    maclient1.login()
                    maclient1.tasker()
                except KeyboardInterrupt:
                    release_socket(maclient1.poster.ht.connections)
                    continue
            elif ch == 'h':
                print(du8('登陆 login/l,设置卡组 set_card/sc,因子战 factor_battle/fcb,秘境探索 explore/e,'
                    '刷列表中的妖精 fairy_battle/fyb,嗑红 red_tea/rt,嗑绿 green_tea/gt,自动卖卡 sell_card/slc,'
                    '设置账号类型 set_server/ss,好友相关 friend/f,转蛋gacha/g,分配点数point/p,礼物盒reward_box/rb,'
                    '手动选择妖精战斗fairy_select/fs,重新登录relogin/rl,问好like/greet/gr,自动配卡as/auto_set; '
                    '\n| 分割多个，空格分隔命令与参数\n'
                    '插件的附加命令:%s\n'
                    '以t:开头可执行任务\n'
                    'http://yooooo.us/2013/maclient' % ','.join(maclient1.plugin.extra_cmd.keys())))
            elif ch == '------':
                print(du8('此功能暂停使用'))
                continue
                # import maclient_plugin_mengsky
                # uname=maclient1._read_config('remote','uname')
                # pwd=maclient1._read_config('remote','pwd')
                # if uname=='':
                #     if maclient1._raw_input('注册新用户？y/n ')=='y':
                #         uname=raw_input('Username >')
                #         pwd=raw_input('Password >')
                #         reg=maRemote.maMengsky(uname=uname,pwd=pwd)
                #         if reg.reg():
                #             print(du8('注册成功！'))
                #         else:
                #             print(du8('注册失败！'))
                #         continue
                #     else:
                #         uname=maclient1._raw_input('Remote-username> ')
                #         if uname.endswith('@maclient'):
                #             uname=uname[:-9]
                #     maclient1._write_config('remote','uname',uname)
                # if pwd=='':
                #     pwd=getpass.getpass('Remote-password> ')
                #     if maclient1._raw_input('是否保存密码(y/n)？')=='y':
                #         maclient1._write_config('remote','pwd',pwd)
                # srv=maRemote.maMengsky(uname=uname,pwd=pwd)
                # if maclient1.set_remote(srv):
                #     dec=maclient1.login()
                #     maclient1.initplayer(dec)
                #     maclient1.tasker()
            elif ch == '2':
                if mod == 0:
                    session = read_proxy()
                    maclient1._write_config('account_%s' % maclient1._read_config('system', 'server'), 'session', session)
                    maclient1.load_cookie()
                    maclient1.login()
                mod = (mod + 1) % 2
            elif ch == '3':
                print(du8('此功能已转移至插件carddeck_edit，你还可以导入MAW卡组配置'))
                print(du8('请到这里查看详细帮助http://t.cn/RvAKyOI'))
                # import maclient_network
                # cards = maclient_network.decode_param(read_proxy(work = 1))
                # cdeck = cards.split('&')[0].split('=')[1].strip('%0A').rstrip(',empty')
                # decks = maclient1._list_option('carddeck')
                # print(du8('选择卡组，输入卡组名以添加新卡组'))
                # print(iter_printer(decks))
                # inp = raw_input("> ")
                # if inp in [str(i) for i in range(1, len(decks) + 1)]:
                #     name = decks[int(inp) - 1]
                # else:
                #     name = inp
                # maclient1._write_config('carddeck', name, cdeck)
                # print(du8('保存到了%s' % name))
            elif ch == '4':
                print(du8('依次输入配置名，值\n输入h查看常用配置,输入e退出'))
                while True:
                    inp = raw_input('> ')
                    if inp == 'h':
                        print(du8('taskname需要程序执行的任务名称，|分割\n'
                                'try_factor_time是刷因子战列表的次数，0为无限\n'
                                'factor_sleep刷列表的间隔(秒)\n'
                                'explore_sleep刷秘境的间隔(秒)\n'
                                'fairy_battle_times刷妖精列表次数\n'
                                'fairy_battle_sleep刷妖精列表间隔(分)\n'
                                'auto_explore是否自动选择秘境,是为1\n'
                                'auto_green_tea,auto_red_tea设置嗑药次数\n'
                                'auto_sell_card 到≥200张了是否自动卖卡\n'
                                'auto_fairy_rewards 自动领取妖精奖励\n'
                                'sell_card_warning 卖卡提醒'))
                    elif inp == 'e':
                        break
                    else:
                        try:
                            p1, p2 = inp.split(' ')
                        except:
                            logging.error('输入有误www')
                        else:
                            if p1 in maclient1._list_option('system'):
                                maclient1._write_config('system', p1, p2)
                            elif p1 in maclient1._list_option('tactic'):
                                maclient1._write_config('tactic', p1, p2)
                            else:
                                logging.error('配置项不存在www')
                                continue
                            print(du8('已保存~'))
                            maclient1.load_config()
            elif ch == '5':
                maclient1.login()
                print(du8('更新游戏数据(g/默认)还是倍卡数据(b)?'))
                inp = raw_input('> ') or 'g'
                import maclient_update
                if inp == 'g':
                    logging.info('将强制重新从服务器下载数据……')
                    crev, irev, brev, cbrev = maclient_update.update_master(maclient1.loc[:2], (True, True, True, True), maclient1.poster)
                    logging.info('%s%s%s%s' % (
                            '卡片数据更新为rev.%s' % crev if crev else '',
                            '道具数据更新为rev.%s' % irev if irev else '',
                            '强敌数据更新为rev.%s' % brev if brev else '',
                            'Combo数据更新为rev.%s' % cbrev if cbrev else ''))
                elif inp == 'b':
                    logging.info('将从多玩数据库下载倍卡信息……')
                    getnew = maclient_update.update_multi(maclient1.loc[:2])
                    if not getnew:
                        logging.warning('无法获得倍卡信息\n对于国服/台服以外的用户请使用am或add_multi命令添加倍卡')
                    else:
                        logging.info('获得%d条倍卡信息' % getnew)
                # the following is deprecated
                # getPATH0=lambda:opath.split(sys.argv[0])[1].find('py') != -1\
                #  and sys.path[0].decode(sys.getfilesystemencoding()) \
                #  or sys.path[1].decode(sys.getfilesystemencoding())#pyinstaller build
                # rev=open(opath.join(getPATH0(),'db/revision.txt'),'r').read().strip('\n').split(',')
                # h={'User-Agent':'maclient/%f'%__version__}
                # upd=macs('/db/revision.txt')[1].strip('\n').split(',')
                # if upd[0]!=rev[0] or upd[1]!=rev[1]:
                #     if upd[1]!=rev[1]:
                #         print(du8('正在更新台服数据……'))
                #         c=macs('/db/card.tw.txt')[1]
                #         open(opath.join(getPATH0(),'db/card.tw.txt'),'w').write(c)
                #         print(du8('卡组更新成功XD'))
                #         c=macs('/db/item.tw.txt')[1]
                #         open(opath.join(getPATH0(),'db/item.tw.txt'),'w').write(c)
                #     if upd[0]!=rev[0]:
                #         print(du8('正在更新国服数据……'))
                #         c=macs('/db/card.cn.txt')[1]
                #         open(opath.join(getPATH0(),'db/card.cn.txt'),'w').write(c)
                #         print(du8('卡组更新成功XD'))
                #         c=macs('/db/item.cn.txt')[1]
                #         open(opath.join(getPATH0(),'db/item.cn.txt'),'w').write(c)
                #     print(du8('道具更新成功XD'))
                #     open(opath.join(getPATH0(),'db/revision.txt'),'w').write(','.join(upd))
                # else:
                #     print(du8('木有更新www'))

            elif ch == '6':
                maclient1._exit(0)
            elif ch != '':
                if ch.startswith('ss') or ch.startswith('set_server') or ch.startswith('l ') or ch.startswith('login') \
                    or ch.startswith('relogin') or ch.startswith('rl'):
                    maclient1.tasker(cmd = ch)
                else:
                    if not maclient1.player_initiated:
                        maclient1.login()
                    try:
                        if ch.startswith('t:'):
                            maclient1.tasker(taskname = ch[2:])
                        else:
                            maclient1.tasker(cmd = ch)
                    except KeyboardInterrupt:
                        release_socket(maclient1.poster.ht.connections)
                        continue
            else:
                maclient.logging.error(du8('嗯-v-？'))
            print(' %s %s' % ('-' * (getTerminalSize()[0] - 2), '\n'))

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception:
        traceback_info = "".join(traceback.format_exception(*sys.exc_info()))
        logging.warning('出错了妈蛋:\n%s' % traceback_info)
        if raw_inputd('***是否提交错误信息以供除错？***\n隐私策略 http://t.cn/RvI6hXS\ny/n > ').lower() == 'y':
            postername = raw_inputd('输入你的昵称(可不填):')
            comment = raw_inputd('输入你的问题描述(可不填):')
            num = None
            while True:
                num = bug_reporter(traceback_info, comment = comment, poster = postername)
                if num or raw_inputd('上传出错，是否重试？ y/n >').lower() == 'n':
                    break
            if num:
                logging.info('\n你的错误信息编号为%s，请提供给开发者处理' % num)
        raw_inputd('***按回车键退出***')
