#!/usr/bin/env python
# coding:utf-8
# A MA emulator "UI"
# Contributor:
#      fffonion        <fffonion@gmail.com>
import sys
import time
import httplib2
import os
import os.path as opath
import threading
import maclient
import maclient_proxy
import maclient_logging
import maclient_remote
import getpass
__version__=1.40
du8=lambda str:str.decode('utf-8')
def iter_printer(l,sep='\n'):
    cnt=1
    str=''
    for e in l:
        str+='%d.%-10s%s'%(cnt,e.strip('\n'),(cnt%3 and '' or sep))
        cnt+=1
    return str.decode('utf-8')
def getTerminalSize():
    #http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
    if os.name=='nt':
        env = os.environ
        dres=None
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
            return None
    else:
        x,y=os.popen('stty size', 'r').read().split()
        return int(y),int(x)

def deck_editor(maclient1):
    return

class srv(threading.Thread):
    def __init__(self, server):
        self.server=server
        threading.Thread.__init__(self)
    def run(self):
        self.server.serve_forever()  
        

def read_proxy(work=0):
    serverport=23300
    server_address = ("", serverport) 
    hdl=maProxy.Handler 
    server = maProxy.ThreadingHTTPServer(server_address,hdl )  
    # Random Target Proxy Server 
    if work==0:
        print(du8('请将设备的代理设置为 本机ip:%s 然后随便进行一次操作' % (serverport)))
    elif work==1:
        print(du8('请将设备的代理设置为 本机ip:%s 然后设定一次卡组\n除了这种办法，你还可以直接在config.ini中输入所需卡片的卡片id，如小狼女: 124\n可以在db/card.tw.txt或db/card.tw.txt中查找' % (serverport)))
    srver=srv(server)
    srver.setDaemon(True) 
    srver.start()
    while True:
        if work==0 and os.path.exists('.session'):
            sessionid=open('.session','r').read()
            print('found sessionid :%s'%sessionid)
            srver.join(1)
            os.remove('.session')
            return sessionid
        elif work==1 and os.path.exists('.carddeck'):
            carddeck=open('.carddeck','r').read()
            print('found carddeck change')
            srver.join(1)
            os.remove('.carddeck')
            return carddeck
        time.sleep(1)
def macs(uri,header={},body='',method='GET'):
    header.update({'User-Agent':'maclient/%f'%__version__})
    try:
        resp,ct=ht.request('%s/%s'%(server,uri),body=body,method=method,headers=header)
    except:
        resp,ct=ht.request('%s/%s'%('http://mac.3owl.com',uri),body=body,method=method,headers=header)
    return resp,ct
def _calc(str):
    import hashlib
    return hashlib.md5(hashlib.md5('9801931maclient---%s---maclient12378138'%str).hexdigest()).hexdigest()
def auth():
    return
    
            



if __name__=='__main__':
    logging=maclient_logging.logging
    reload(sys)
    sys.setdefaultencoding('utf-8')
    ht=httplib2.Http(timeout=30)
    intro='v%s%s'%(__version__,os.name=='nt' and ' by fffonion' or '')
    print(du8('%s%s%s%s'%('='*((getTerminalSize()[0]-len(intro)-18)/2),'丧心病狂的MA客户端',intro,'='*((getTerminalSize()[0]-len(intro)-18)/2))))
    if len(sys.argv)>2:
        maclient1=maclient.maClient(configfile=sys.argv[1],savesession=True)
        dec=maclient1.login()
        maclient1.initplayer(dec)
        arg=' '.join(sys.argv[2:])
        pos=arg.find('t:')
        if pos!=-1:
            maclient1.tasker(taskname=arg[pos+2:])
        else:
            maclient1.tasker(cmd=arg)
    else:
        if len(sys.argv)==2:
            maclient1=maclient.maClient(configfile=sys.argv[1],savesession=True)
        else:
            maclient1=maclient.maClient(savesession=True)
        #进入游戏
        #maclient1._dopost('post_token',postdata=ma.encode_param('S=nosessionid&login_id=%s&password=%s&app=and&token=BubYIgiyDYTFUifydHIoIOGBiujgRzrEFUIbIKOHniHIoihoiHasbdhasbdUIUBujhbjhjBJKJBb'%(username,password)),usecookie=True,extraheader={'Cookie2': '$Version=1'})
        #登陆
        server=maclient1._read_config('remote','maCServer') or 'http://mac.yooooo.us'
        
        auth()
        mode=['普通','同时在线']
        mod=0
        while True:
            print(du8('This is a kingdom\'s junction. Tell me your select.【Mode:%s Server:%s】\n\n1.进入游戏\t\t[快速通道]\n2.遥控器模式[NEW]\te.刷秘境\n3.切换模式->%s\tfyb.刷妖精\n4.编辑卡组\t\tfcb.因子战\n5.编辑配置\t\tf.好友相关\n6.更新数据库\t\th.命令速查\n7.退出'%(mode[mod],maclient1._read_config('system','server'),mode[(mod+1)%2])))
            ch=raw_input('Select> ')
            if ch=='1' or ch =='':
                dec=maclient1.login()
                maclient1.initplayer(dec)
                maclient1.tasker()
            elif ch=='h':
                print(du8('登陆 login/l,设置卡组 set_card/sc,因子战 factor_battle/fcb,秘境探索 explore/e,刷列表中的妖精 fairy_battle/fyb,嗑药 red_tea/rt,嗑药 green_tea/gt,自动卖卡 sell_card/slc,设置账号类型 set_server/ss,好友相关 friend/f,转蛋gacha/g; | 分割多个，空格分隔命令与参数\n以t:开头可执行任务\nContact:http://www.yooooo.us'))
            elif ch=='2':
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
            elif ch=='3':
                if mod==0:
                    session=read_proxy(work=0)
                    maclient1._write_config('account_%s'%maclient1._read_config('system','server'),'session',session)
                mod=(mod+1)%2
            elif ch =='4':
                cards=ma.decode_param(read_proxy(work=1))
                cdeck=cards.split('&')[0].split('=')[1].strip('%0A')
                while cdeck.endswith('empty'):
                    cdeck=cdeck.rstrip(',empty')
                decks=maclient1._list_option('carddeck')
                print(du8('选择卡组，输入卡组名以添加新卡组'))
                print(iter_printer(decks))
                inp=raw_input("> ")
                if inp in [str(i) for i in range(1,len(decks)+1)]:
                    name=decks[int(inp)-1]
                else:
                    name=inp
                maclient1._write_config('carddeck',name,cdeck)
                print(du8('保存到了%s'%name))
            elif ch =='5':
                print(du8('依次输入配置类别，配置名，值；如设置自动嗑红茶3次 auto_red_tea 3\n输入h查看列表'))
                inp=raw_input('> ')
                if inp=='h':
                    print(du8('''taskname需要程序执行的任务名称，|分割
try_factor_time是刷因子战列表的次数，0为无限
factor_sleep刷列表的间隔(秒)
explore_sleep刷秘境的间隔(秒)
fairy_battle_times刷妖精列表次数
fairy_battle_sleep刷妖精列表间隔(分)
auto_explore是否自动选择秘境,是为1
auto_green_tea,auto_red_tea设置嗑药次数
auto_sell_card 到≥200张了是否自动卖卡
auto_fairy_rewards 自动领取妖精奖励
sell_card_warning 卖卡提醒'''))
                else:
                    try:
                        p1,p2=inp.split(' ')
                    except:
                        logging.error('输入有误www')
                    else:
                        maclient1._write_config('system',p1,p2)
                        print(du8('已保存~'))
            elif ch =='6':
                getPATH0=lambda:opath.split(sys.argv[0])[1].find('py') != -1\
                 and sys.path[0].decode(sys.getfilesystemencoding()) \
                 or sys.path[1].decode(sys.getfilesystemencoding())#pyinstaller build
                rev=open(opath.join(getPATH0(),'db/revision.txt'),'r').read().strip('\n').split(',')
                h={'User-Agent':'maclient/%f'%__version__}
                upd=macs('/db/revision.txt')[1].strip('\n').split(',')
                if upd[0]!=rev[0] or upd[1]!=rev[1]:
                    if upd[1]!=rev[1]:
                        print(du8('正在更新台服数据……'))
                        c=macs('/db/card.tw.txt')[1]
                        open(opath.join(getPATH0(),'db/card.tw.txt'),'w').write(c)
                        print(du8('卡组更新成功XD'))
                        c=macs('/db/item.tw.txt')[1]
                        open(opath.join(getPATH0(),'db/item.tw.txt'),'w').write(c)
                    if upd[0]!=rev[0]:
                        print(du8('正在更新国服数据……'))
                        c=macs('/db/card.cn.txt')[1]
                        open(opath.join(getPATH0(),'db/card.cn.txt'),'w').write(c)
                        print(du8('卡组更新成功XD'))
                        c=macs('/db/item.cn.txt')[1]
                        open(opath.join(getPATH0(),'db/item.cn.txt'),'w').write(c)
                    print(du8('道具更新成功XD'))
                    open(opath.join(getPATH0(),'db/revision.txt'),'w').write(','.join(upd))
                else:
                    print(du8('木有更新www'))
                
            elif ch =='7':
                sys.exit(0)
            elif ch!='':
                if ch.startswith('ss') or ch.startswith('set_server') or ch.startswith('l ') or ch.startswith('login'):
                    maclient1.tasker(cmd=ch)
                else:
                    dec=maclient1.login()
                    maclient1.initplayer(dec)
                    if ch.startswith('t:'):
                        maclient1.tasker(taskname=ch[2:])
                    else:
                        maclient1.tasker(cmd=ch)
            else:
                maclient.logging.error(du8('嗯-v-？'))
            print(' %s %s'%('-'*(getTerminalSize()[0]-2),'\n'))
raw_input('THAT\'S THE END')