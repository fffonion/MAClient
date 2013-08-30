#!/usr/bin/env python
# coding:utf-8
# maclient!
# Contributor:
#      fffonion        <fffonion@gmail.com>
from __future__ import print_function
import os
import os.path as opath
import re
import sys
import time
import locale
import base64
from xml2dict import XML2Dict
import random
import ConfigParser
import threading
import getpass
import maclient_player
import maclient_network
import maclient_logging
__version__=1.41
#CONSTS:
CARD_NORM,CARD_MAX,CARD_NORM_HOLO,CARD_MAX_HOLO=0,1,2,3
EXPLORE_BATTLE,NORMAL_BATTLE=0,1

GACHA_FRIENNSHIP_POINT,GACHA_GACHA_TICKET,GACHA_11=1,2,4
SERV_CN,SERV_CN2,SERV_TW='cn','cn2','tw'
#eval dicts
eval_fairy_select={'LIMIT':'time_limit','NOT_BATTLED':'not_battled','.lv':'.fairy.lv','IS_MINE':'user.id == self.player.id','IS_WAKE':'wake','STILL_ALIVE':"self.player.fairy['alive']"}
eval_fairy_select_carddeck={'IS_MINE':'discoverer_id == self.player.id','IS_WAKE':'rare_flg=="1"','STILL_ALIVE':"self.player.fairy['alive']",'LIMIT':'time_limit'}
eval_explore_area={'IS_EVENT':"area_type=='1'",'IS_DAILY_EVENT':"id.startswith('5')",'NOT_FINNISHED':"prog_area!='100'",\
            }
eval_explore_floor={'NOT_FINNISHED':'progress!="100"'}
eval_select_card={'lv':'lv_i','hp':'hp_i','atk':'atk_i'}
eval_task={}
duowan={'cn':'http://db.duowan.com/ma/cn/card/detail/%s.html','tw':'http://db.duowan.com/ma/card/detail/%s.html'}
logging = maclient_logging.Logging('logging')#=sys.modules['logging']
du8=lambda str:str.decode('utf-8')#.encode(locale.getdefaultlocale()[1], 'error')
def setT(strt):
    os.system('TITLE %s'%strt.decode('utf-8').encode('gbk','ignore'))

class set_title(threading.Thread):
    def __init__(self,maInstance):
        threading.Thread.__init__(self)
        self.maInstance=maInstance
        self.flag=1
    def run(self):
        if not self.maInstance.settitle:
            self.flag=0
       # if os.name == 'nt':
        while self.flag==1:
            self.maInstance.player.calc_ap_bc()
            strt='[%s] AP:%d/%d BC:%d/%d G:%d FP:%d Cards:%d'%(self.maInstance.player.name,self.maInstance.player.ap['current'],self.maInstance.player.ap['max'],self.maInstance.player.bc['current'],self.maInstance.player.bc['max'],self.maInstance.player.gold,self.maInstance.player.friendship_point,self.maInstance.player.card.count)
            setT(strt)
            time.sleep(28)
        #elif os.name == 'posix':
         #   pass

class conn_ani(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.flag=1
    def run(self):
        cnt=0
        while self.flag==1:
            print('Connecting.%s%s%s'%('.'*cnt,' '*(3-cnt),'\b'*20),end='')
            cnt=(cnt+1)%4
            time.sleep(0.15)

class maClient():
    def __init__(self,configfile='',savesession=False):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.getPATH0=lambda:opath.split(sys.argv[0])[1].find('py') != -1\
         and sys.path[0].decode(sys.getfilesystemencoding()) \
         or sys.path[1].decode(sys.getfilesystemencoding())#pyinstaller build
        self.cf=ConfigParser.ConfigParser()
        if configfile=='':
            if not os.path.exists(self.getPATH0()+opath.sep+'config.ini'):
                print(du8('正在尝试以默认配置文件启动，但该文件(config.ini)不存在'))
                self._exit(1)
            self.configfile=self.getPATH0()+opath.sep+'config.ini'
        else:
            self.configfile=configfile
        self.cf.read(self.configfile)
        #configurations
        self.loc=self._read_config('system','server')
        self.playerfile='.%s.playerdata'%self.loc
        self.username=self._read_config('account_%s'%self.loc,'username')
        self.password=self._read_config('account_%s'%self.loc,'password')
        self.cfg_auto_explore=not self._read_config('system','auto_explore')=='0'
        self.cfg_auto_sell=not self._read_config('system','auto_sell_cards')=='0'
        self.cfg_auto_gacha=not self._read_config('system','auto_fp_gacha')=='0'
        self.cfg_auto_fairy_rewards=not self._read_config('system','auto_fairy_rewards')=='0'
        self.cfg_auto_build= self._read_config('system','auto_fp_gacha')=='1' and '1' or '0'
        self.cfg_fp_gacha_buld=self._read_config('system','fp_gacha_bulk')=='1' and '1' or '0'
        self.cfg_sell_card_warning=int(self._read_config('system','sell_card_warning') or '1')
        self.cfg_auto_rt_level=self._read_config('system','auto_red_tea_level')
        self.cfg_strict_bc=self._read_config('system','strict_bc')=='1'
        self.cfg_fairy_final_kill_hp=int(self._read_config('system','fairy_final_kill_hp') or '20000')
        logging.basicConfig(level=self._read_config('system','loglevel'))
        logging.setlogfile('events_%s.log'%self.loc)
        self.cfg_save_session=savesession
        self.cfg_delay=float(self._read_config('system','delay'))
        self.cfg_display_ani=(self._read_config('system','display_ani') or '1')=='1'
        self.settitle=os.name=='nt'
        self.posttime=0
        self.set_remote(None)
        ua=self._read_config('system','user-agent')
        if ua!='':
            logging.debug('system:ua changed to %s'%(ua))
        self.poster=maclient_network.poster(self,self.loc,logging,ua)
        self.cookie=self._read_config('account_%s'%self.loc,'session')
        self.poster.set_cookie(self.cookie)
        #eval
        etmp=self._read_config('condition','fairy_select') or 'True'
        self.evalstr_fairy=self._eval_gen(
            '(%s) and fairy.put_down in ["0","1"]'%etmp,
            eval_fairy_select)#1战斗中 2胜利 3失败
        self.evalstr_area=self._eval_gen(self._read_config('condition','explore_area'),eval_explore_area)
        self.evalstr_floor=self._eval_gen(self._read_config('condition','explore_floor'),eval_explore_floor)
        self.evalstr_selcard=self._eval_gen(self._read_config('condition','select_card_to_sell'),eval_select_card)
        self.evalstr_fairy_select_carddeck=self._eval_gen(self._read_config('condition','fairy_select_carddeck'),
            eval_fairy_select_carddeck)
        self.evalstr_factor=self._eval_gen(self._read_config('condition','factor'),{})
        #tasker须动态生成#self.evalstr_task=self._eval_gen(self._read_config('system','tasker'),{})
        logging.debug(du8('system:初始化完成(%s)'%self.loc))
        self.lastposttime=time.time()
        self.player_initiated=False
    def set_remote(self,remoteInstance):
        self.remote=remoteInstance
        self.remoteHdl=(self.remote ==None and (lambda method=None,fairy='':True) or self.remote_Hdl_())
        if self.remote !=None:
            res,msg=self.remote.login()
            if res:
                logging.debug('remote_hdl:%s'%msg)
                return True
            else:
                logging.warning('remote_hdl:%s'%msg)
                return False  
    def _dopost(self,urikey,postdata='',usecookie=True,setcookie=True,extraheader={'Cookie2': '$Version=1'},checkerror=True,noencrypt=False):
        self.remoteHdl()
        if self.cfg_display_ani:
            connani=conn_ani()
            connani.setDaemon(True)
            connani.start()
        if time.time()-self.lastposttime<=self.cfg_delay:
            if  self.cfg_delay==0:
                logging.warning('post:NO DELAY!')
            else:
                logging.debug('post:slow down...')
                time.sleep(random.random()*self.cfg_delay)
            self.lastposttime=time.time()
        resp,dec=self.poster.post(urikey,postdata,usecookie,setcookie,extraheader,noencrypt)
        if self.cfg_display_ani:
            connani.flag=0
            connani.join(0.16)
        if int(resp['status'])>=400:
            return resp,dec
        if checkerror:
            err=XML2Dict().fromstring(dec).response.header.error
            resp.update({'error':False,'errno':0,'errmsg':''})
            if err.code!='0':
                resp['errmsg']=err.message
                #1050木有BC 1010卖了卡 8000无法进行当前操作
                if not err.code in ['1050','1010']:
                    logging.error('code:%s msg:%s'%(err.code,err.message))
                    resp.update({'error':True,'errno':int(err.code)})
                if err.code == '9000':
                    self._write_config('account_%s'%self.loc,'session','')
                    logging.info(du8('A一个新的小饼干……'))
                    self.login(fast=True)
                    return self._dopost(urikey,postdata,usecookie,setcookie,extraheader,checkerror,noencrypt)
            else:
                resp.update({'error':False})
        else:
            resp.update({'error':False})
        if setcookie and 'set-cookie' in resp:
            self._write_config('account_%s'%self.loc,'session',resp['set-cookie'].split(',')[-1].rstrip('path=/').strip())
        if self.player_initiated :
            #auto check cards and fp
            if not self.auto_check(urikey):
                logging.error(du8('由于以上↑的原因，无法继续执行！'))
                self._exit(1)
            update_dt=self.player.update_all(dec)
            #update profile
            if not resp['error']:
                self.remoteHdl(method='PROFILE')
                if self.settitle:
                    setT('[%s] AP:%d/%d BC:%d/%d G:%d FP:%d Cards:%d'%(self.player.name,self.player.ap['current'],self.player.ap['max'],self.player.bc['current'],self.player.bc['max'],self.player.gold,self.player.friendship_point,self.player.card.count))
                else:
                    if self.posttime==5:
                        logging.inform(du8('汇报')+' AP:%d/%d BC:%d/%d G:%d FP:%d '%(self.player.ap['current'],self.player.ap['max'],self.player.bc['current'],self.player.bc['max'],self.player.gold,self.player.friendship_point))
                    self.posttime=(self.posttime+1)%6
                if update_dt[1]:
                    logging.debug(update_dt[0])
                    open(self.playerfile,'w').write(dec)
                    logging.debug('post:master cards saved.')
        return resp,dec

    def _read_config(self,sec,key):
        if not self.cf.has_section(sec):
            self.cf.add_section(sec) 
        if self.cf.has_option(sec, key):
            val=self.cf.get(sec, key)
            if sys.platform=='win32':val=val.decode('cp936').encode('utf-8')
        else:
            val=''
        if val=='':return ''
        else:return val

    def _write_config(self,sec,key,val):
        if not self.cf.has_section(sec):
            self.cf.add_section(sec)
        self.cf.set(sec, key,val)
        f=open(self.configfile, "w")
        self.cf.write(f)
        f.flush()

    def _list_option(self,sec):
        return self.cf.options(sec)

    def _del_option(self,sec,key):
        f=self.configfile
        self.cf.read(f)
        self.cf.remove_option(sec, key)
        self.cf.write(open(f, "w"))

    def _eval_gen(self,str,repldict={}):
        repldict2={'hour':"int(time.strftime('%H',time.localtime(time.time())))",'minute':"int(time.strftime('%M',time.localtime(time.time())))",'BC':'self.player.bc["current"]','AP':'self.player.ap["current"]','G':'self.player.gold','FP':'self.friendship_point','FAIRY_ALIVE':'self.player.fairy["alive"]'}
        if str=='':
            return 'True'
        for i in repldict:
            str=str.replace(i,repldict[i])
        for i in repldict2:
            str=str.replace(i,repldict2[i])
        return str

    
    def _raw_input(self,str):
        return raw_input(du8(str).encode(locale.getdefaultlocale()[1] or 'utf-8', 'replace'))
    
    def tasker(self,taskname='',cmd=''):
        cnt=int(self._read_config('system','tasker_times') or '1')
        if cnt==0:
            cnt=9999999
        if taskname =='':
            taskname=self._read_config('system','taskname')
            if taskname=='':
                logging.info(du8('没有配置任务！'))
                return
        if  cmd !='':
            tasks=cmd
            cnt=1
        taskeval=self._eval_gen(self._read_config('tasker',taskname),eval_task)
        for c in xrange(cnt):
            logging.debug('tasker:loop %d/%d'%(c+1,cnt)) 
            if cmd=='':
                tasks=eval(taskeval)
                logging.debug('tasker:eval:%s result:%s'%(taskeval,tasks))
            for task in tasks.split('|'):
                task=(task+' ').split(' ')
                logging.debug('tasker:%s'%task[0])
                task[0]=task[0].lower()
                if task[0]=='set_card' or task[0]=='sc':
                    if task[1]=='':
                        logging.error('set_card need 1 argument')
                    else:
                        self.set_card(task[1])
                elif task[0]=='explore' or task[0]=='e':
                    self.explore(' '.join(task[1:]))
                elif task[0]=='factor_battle' or task[0]=='fcb':
                    self.factor_battle(' '.join(task[1:]))
                elif task[0]=='fairy_battle' or task[0]=='fyb':
                    self.fairy_battle_loop(task[1])
                elif task[0]=='fairy_select' or task[0]=='fs':
                    self.fairy_select(cond=task[1:])
                elif task[0]=='green_tea' or task[0]=='gt':
                    self.green_tea()
                elif task[0]=='red_tea' or task[0]=='rt':
                    self.red_tea()
                elif task[0]=='sell_card' or task[0]=='slc':
                    self.select_card_sell(' '.join(task[1:]))
                elif task[0]=='set_server' or task[0]=='ss':
                    self._write_config('system','server',task[1])
                    self.loc=task[1]
                elif task[0]=='relogin' or task[0]=='rl':
                    self._write_config('account_%s'%self.loc,'session','')
                    self.login()
                elif task[0]=='login' or task[0]=='l':
                    if len(task)==2:
                        task.append('')
                    dec=self.login(uname=task[1],pwd=task[2])
                    self.initplayer(dec)
                elif task[0]=='friend' or task[0]=='f':
                    if len(task)==2:
                        task=[task[0],'','']
                    self.friends(task[1],task[2]=='True')
                elif task[0]=='point' or task[0]=='p':
                    self.point_setting()
                elif task[0]=='rb' or task[0]=='reward_box':
                    self.reward_box()
                elif task[0]=='gacha' or task[0]=='g':
                    if len(task)==2:
                        task[1]=GACHA_FRIENNSHIP_POINT
                    else:
                        task[1]=int(task[1])
                    self._gacha(gacha_type=task[1])
                else:
                    logging.warning('command "%s" not recognized.'%task[0])
                if cnt!=1:
                    logging.inform(du8('tasker:正在滚床单wwww'))
                    time.sleep(3.15616546511)
                    resp,ct=self._dopost('mainmenu')#初始化

    def login(self,uname='',pwd='',fast=False):

        sessionfile='.%s.session'%self.loc
        if os.path.exists(self.playerfile) and self._read_config('account_%s'%self.loc,'session')!='' and uname=='':
            logging.info(du8('加载了保存的账户XD'))
            dec=open(self.playerfile,'r').read()
        else:
            self.username= uname or self.username
            self.password= pwd or self.password
            if self.username=='':
                self.username=self._raw_input('Username:')
            if self.password=='' or (uname!='' and pwd==''):
                self.password=getpass.getpass('Password:')
                if self._raw_input('是否保存密码(y/n)？')=='y':
                    self._write_config('account_%s'%self.loc,'password',self.password)
                    logging.warning(du8('保存的登录信息没有加密www'))
            token=self._read_config('system','device_token').replace('\\n','\n') or \
            'nuigiBoiNuinuijIUJiubHOhUIbKhuiGVIKIhoNikUGIbikuGBVININihIUniYTdRTdREujhbjhj'
            if not fast:
                self._dopost('check_inspection',checkerror=False,extraheader={},usecookie=False)
                self._dopost('notification/post_devicetoken',postdata='S=%s&login_id=%s&password=%s&app=and&token=%s'%('nosessionid',self.username,self.password,token),checkerror=False)
            
            resp,dec=self._dopost('login',postdata='login_id=%s&password=%s'%(self.username,self.password))
            if resp['error']:
                logging.info(du8('登录失败しました'))
                self._exit(1)
            else:
                logging.info(du8('[%s] 登录成功!'%self.username))
                self._write_config('account_%s'%self.loc,'username',self.username)
                open(self.playerfile,'w').write(dec)
                self._write_config('record','last_set_card','')
                self._write_config('record','last_set_bc','0')
        return dec
        
    def initplayer(self,xml):
        self.player=maclient_player.player(xml,self.loc)
        self.carddb=self.player.card.db
        self.itemdb=self.player.item.name
        self.player_initiated=True
        if self.player.id!='0':
            self._write_config('account_%s'%self.loc,'user_id',self.player.id)
        else:
            self.player.id=self._read_config('account_%s'%self.loc,'user_id')
        if self.settitle:
            #窗口标题线程
            self.stitle=set_title(self)
            self.stitle.setDaemon(True)
            self.stitle.start()

    def auto_check(self,doingwhat):
        if not doingwhat in ['login','check_inspection','notification/post_devicetoken','card/exchange', 'trunk/sell','roundtable/edit','cardselect/savedeckcard']:
            if int(self.player.card.count) >=200:
                if self.cfg_auto_sell:
                    logging.inform(du8('卡片放满了，自动卖卡 v(￣▽￣*)'))
                    self.select_card_sell()
                    return True
                else:
                    logging.warning(du8('卡片已经放不下了，请自行卖卡www'))
                    return False
            if self.player.friendship_point>=9900 and \
                not doingwhat in ['gacha/buy','gacha/select/getcontents']:
                if self.cfg_auto_gacha:
                    logging.inform(du8('绊点有点多，自动转蛋(*￣▽￣)y '))
                    self._gacha(gacha_type=GACHA_FRIENNSHIP_POINT)
                    return True
                else:
                    logging.warning(du8('绊点已经很多，请自行转蛋消耗www'))
                    return False
        return True

    def check_strict_bc(self,refresh=False):
        if not self.cfg_strict_bc:
            return False
        last_set_bc=self._read_config('record','last_set_bc') or '0'
        last_set_bc=int(last_set_bc)
        if self.player.bc['current']<last_set_bc:
            logging.warning(du8('strict_bc:严格BC模式已触发www'))
            return True
        else:
            logging.debug('strict_bc:nothing happened~')
            return False


    def set_card(self,deckkey):
        if deckkey=='no_change':
            logging.debug('set_card:no_change!')
            return False
        cardid=self._read_config('carddeck',deckkey)
        if cardid==self._read_config('record','last_set_card'):
            logging.debug('set_card:card deck satisfied, not changing.')
            return False
        if cardid =='':
            logging.warning('set_card:unset carddeck key?')
            return False
        cardid=cardid.split(',')
        param=[]
        last_set_bc=0
        leader_card=0
        for i in xrange(len(cardid)):
            if cardid[i]=='empty':
                param.append('empty')
                leader_card+=1
            elif len(cardid[i])>3:
                param.append(cardid[i])
                mid=self.player.card.sid(cardid[i]).master_card_id
                last_set_bc+=int(self.carddb[int(mid)][2])
            else:
                c=self.player.card.cid(cardid[i])
                if c!=[]:
                    param.append(c[-1].serial_id)
                    last_set_bc+=int(self.carddb[int(cardid[i])][2])
                else:
                    logging.error(du8('你木有 id为 %s (%s)的卡片'%(cardid[i],self.carddb[int(cardid[i])][0])))
        param=param+['empty']*(12-len(param))
        while True:
            if param==['empty']*12:
                break
            if self._dopost('roundtable/edit',postdata='move=1')[0]['error']:
                break
            t=random.randint(5,10)
            logging.inform(du8('休息%d秒，假装在找卡'%t))
            time.sleep(t)
            postparam='C='+','.join(param)+'&lr='+param[leader_card]
            if self._dopost('cardselect/savedeckcard',postdata=postparam)[0]['error']:
                break
            logging.info(du8('成功更换卡组为%s cost%d'%(deckkey,last_set_bc)))
            #保存
            self._write_config('record','last_set_card',self._read_config('carddeck',deckkey))
            #记录BC
            self._write_config('record','last_set_bc',str(last_set_bc))
            return True
        logging.info(du8('卡组没有改变'))
        return False


    def _use_item(self,itemid):
        param='item_id=%s'%itemid
        resp,ct=self._dopost('item/use',postdata=param)
        if resp['error']:
            return False
        else:
            logging.info(du8('使用了道具 ')+self.itemdb[int(itemid)])
            logging.debug('useitem:item %s : %s left'%(itemid,self.player.item.count[int(itemid)]))
            return True

    def red_tea(self,silent=False):
        auto=int(self._read_config('system','auto_red_tea') or '0')
        if auto>0:
            self._write_config('system','auto_red_tea',str(auto-1))
            res=self._use_item('2')
        else:
            if silent:
                logging.debug('red_tea:auto mode, let it go~')
                return False
            else:
                if self._raw_input(du8('来一坨红茶？ y/n '))=='y':
                    res=self._use_item('2')
        if res:
            self.player.bc['current']=self.player.bc['max']
        return res

    def green_tea(self,silent=False):
        auto=int(self._read_config('system','auto_green_tea') or '0')
        if auto>0:
            self._write_config('system','auto_green_tea',str(auto-1))
            res=self._use_item('1')
        else:
            if silent:
                logging.debug('green_tea:auto mode, let it go~')
                return False
            else:
                if self._raw_input(du8('嗑一瓶绿茶？ y/n '))=='y':
                    res=self._use_item('1')
        if res:
            self.player.ap['current']=self.player.ap['max']
        return res

    def explore(self,cond=''):
        #选择秘境
        has_boss=[]
        while True:
            resp,ct=self._dopost('exploration/area')
            if resp['error']:
                return
            areas=XML2Dict().fromstring(ct).response.body.exploration_area.area_info_list.area_info
            if not self.cfg_auto_explore:
                for i in xrange(len(areas)):
                    print('%d.%s(%s%%/%s%%) %s'%\
                        (i+1,areas[i].name,areas[i].prog_area,areas[i].prog_item,(areas[i].area_type=='1' and 'EVENT' or '')))
                areasel=[areas[int(self._raw_input('选择： ') or '1')-1]]
            else:
                logging.info(du8('自动选图www'))
                evalstr= (cond!='' and self._eval_gen(cond) or self.evalstr_area)
                areasel=[]
                logging.debug('explore:eval:%s'%(evalstr))
                for area in areas:
                    if eval(evalstr) and not area.id in has_boss:
                        areasel.append(area)
                if areasel==[]:
                    logging.info(du8('没有符合条件的秘境www'))
                    return
            area=areasel[0]
            logging.debug('explore:area id:%s'%area.id)
            logging.info(du8('选择了秘境 ')+area.name)
            while True:
                #选择地区
                param='area_id=%s'%(area.id)
                resp,ct=self._dopost('exploration/floor',postdata=param)
                if resp['error']:
                    return
                floors=XML2Dict().fromstring(ct).response.body.exploration_floor.floor_info_list.floor_info
                if 'found_item_list' in floors:
                    floors=[floors]#只有一个
                nofloorselect=True
                logging.debug('explore:eval:%s'%(self.evalstr_floor))
                for floor in floors:
                    floor.cost=int(floor.cost)
                    floor.cost=int(floor.cost)
                    if eval(self.evalstr_floor):
                        nofloorselect=False
                        break
                if nofloorselect:
                    break#更换秘境
                if floor.type=='1':
                    logging.warning(du8('秘境守护者出现，请手动干掉之www；将忽略此秘境'))
                    has_boss.append(area.id)
                    break
                logging.info(du8('进♂入地区 ')+floor.id)
                #进入
                param='area_id=%s&check=1&floor_id=%s'%(area.id,floor.id)
                if self._dopost('exploration/get_floor',postdata=param)[0]['error']:
                    return
                #走路
                param='area_id=%s&auto_build=1&floor_id=%s'%(area.id,floor.id)
                while True:
                    resp,ct=self._dopost('exploration/explore',postdata=param)
                    if resp['error']:
                        return
                    info=XML2Dict().fromstring(ct).response.body.explore
                    logging.debug('explore:event_type:'+info.event_type)
                    if info.event_type!='6':
                        logging.info(du8('获得:%sG %sEXP, 进度:%s, 升级剩余:%s'%(info.gold,info.get_exp,info.progress,info.next_exp)))
                        #0,19似乎都是没事
                        if info.event_type=='1':
                            '''<fairy>
                                    <serial_id>20840184</serial_id>
                                    <master_boss_id>2043</master_boss_id>
                                    <hp_max>753231</hp_max>
                                    <time_limit>7200</time_limit>
                                    <discoverer_id>532554</discoverer_id>
                                    <attacker_history></attacker_history>
                                    <rare_flg>0</rare_flg>
                                    <event_chara_flg>0</event_chara_flg>
                            </fairy>'''
                            info.fairy.lv,info.fairy.hp=int(info.fairy.lv),int(info.fairy.hp)
                            logging.info(du8('碰到只妖精:')+info.fairy.name+' lv%d hp%d'%(info.fairy.lv,info.fairy.hp))
                            logging.debug('sid'+info.fairy.serial_id+' mid'+info.fairy.master_boss_id+' uid'+info.fairy.discoverer_id)
                            self.player.fairy={'id':info.fairy.serial_id,'alive':True}
                            #evalfight=self._eval_gen(self._read_config('condition','encounter_fairy'),\
                            #    {'fairy':'info.fairy'})
                            #logging.debug('eval:%s result:%s'%(evalfight,eval(evalfight)))
                            #if eval(evalfight):
                            logging.inform(du8('3秒后开始战斗www'))
                            time.sleep(3)
                            self._fairy_battle(info.fairy,type=EXPLORE_BATTLE)
                            time.sleep(5.5)
                        if info.event_type=='2':
                            logging.info(du8('碰到个傻X：'+info.encounter.name+' -> '+info.message))
                            time.sleep(1.5)
                        if info.event_type=='3':
                            usercard=info.user_card
                            logging.debug('explore:cid %s sid %s'%(usercard.master_card_id,usercard.serial_id))
                            logging.info(du8('获得了 ')+self.carddb[int(usercard.master_card_id)][0]+
                                (' %s☆')%(self.carddb[int(usercard.master_card_id)][1]))
                        if info.event_type=='15':
                            compcard=info.autocomp_card[-1]
                            logging.debug('explore:cid %s sid %s'%(
                                compcard.master_card_id,
                                compcard.serial_id))
                            logging.info(du8('合成了 ')+self.carddb[int(compcard.master_card_id)][0]+
                                (' lv%s exp%s nextexp%s')%(
                                    compcard.lv,
                                    compcard.exp,
                                    compcard.next_exp))
                        if info.event_type=='5':
                            logging.info(du8('AREA %s CLEAR -v-'%floor.id))
                            time.sleep(2)
                            break
                        if info.event_type=='12':
                            logging.info(du8('AP回复~'))
                        if info.event_type=='13':
                            logging.info(du8('BC回复~'))
                        if info.event_type=='19':
                            try:
                                itemid=info.special_item.item_id
                                itembefore=int(info.special_item.before_count)
                                itemnow=int(info.special_item.after_count)
                                logging.debug('explore:itemid:%s'%(itemid))
                                logging.info(du8('获得收集品[%s] x%d!')%(self.itemdb[int(itemid)],itemnow-itembefore))
                            except KeyError:
                                 logging.debug('explore:item not found?')
                    else:
                        logging.warning(du8('AP不够了TUT'))
                        if not self.green_tea(self.cfg_auto_explore):
                            logging.error(du8('不给喝，不走了o(￣ヘ￣o＃) '))
                            return
                        else:
                            continue
                    if info.lvup=='1':
                        logging.info(du8('升级了：↑')+self.player.lv)
                        time.sleep(3)
                    # if info.progress=='100':
                    #     break
                    time.sleep(int(self._read_config('system','explore_sleep')))

                    #print '%s - %s%% cost%s'%\
                        #(floors[i].id,floors[i].progress,floors[i].cost)
   
    def _gacha(self,gacha_type=GACHA_FRIENNSHIP_POINT):
        if gacha_type==GACHA_FRIENNSHIP_POINT:
            ab=self.cfg_auto_build
            bulk=self.cfg_fp_gacha_buld
        else:
            ab=self._read_config('system','auto_build')
            bulk='0'
        if self._dopost('gacha/select/getcontents')[0]['error']:
            return
        logging.debug("gacha:auto_build:%s bulk:%s product_id:%d"%(ab,bulk,gacha_type))
        param="auto_build=%s&bulk=%s&product_id=%d"%(ab,bulk,gacha_type)
        resp,ct=self._dopost('gacha/buy',postdata=param)
        if resp['error']:
            return
        gacha_buy=XML2Dict().fromstring(ct).response.body.gacha_buy
        excards=gacha_buy.final_result.ex_user_card
        excname=[]
        if 'is_new_card' in excards:
            excards=[excards]
        for card in excards:
            mid=self.player.card.sid(card.serial_id).master_card_id
            if gacha_type>GACHA_FRIENNSHIP_POINT:
                rare=['R','R+','SR','SR+']
                rare_str=' '+rare[self.carddb[int(mid)][1]-3]
            else:
                rare_str=' '
            excname.append('[%s]%s%s'%(
                self.carddb[int(mid)][0],
                self.player.card.sid(card.serial_id).holography =='1' and '-HOLO' or '',
                rare_str
            ))
        
        logging.info(du8('获得%d张新卡片: '%len(excname))+', '.join(excname))
        self.player.friendship_point=self.player.friendship_point-200*len(excname)
        if ab=='1' and 'auto_compound' in gacha_buy:
            try:
                autocompcards=gacha_buy.auto_compound
                if 'compound' in autocompcards:
                    autocompcards=[autocompcards]
                autocname=[]
                for card in autocompcards.compound:
                    mid=card.base_card.master_card_id
                    autocname.append('['+self.carddb[int(mid)][0]+']')
                logging.info(du8('合成了%d张新卡片:'%len(autocname))+', '.join(autocname))
            except:
                logging.debug('gacha:no auto build')
        time.sleep(7.3890560964)

    def _get_rewards(self,notice_id):
        hasgot=False
        while len(notice_id)>0:
            #一次20个
            if len(notice_id)>20:
                logging.debug('_get_rewards:too many rewards (%d)'%(len(notice_id)))
                no_id=notice_id[:20]
            else:
                no_id=notice_id
            notice_id=notice_id[len(no_id):]
            param="notice_id=%s"%(','.join(no_id))
            resp,ct=self._dopost('menu/get_rewards',postdata=param)
            if not resp['error']:
                logging.debug('_get_rewards:get successfully.')
                hasgot=True
        return hasgot,resp['errmsg']

    def select_card_sell(self,cond=''):
        cinfo=[]
        sid=[]
        warning_card=[]
        logging.debug('select_card:eval:%s'%(self.evalstr_selcard))
        for card in self.player.card.cards:
            card.star=int(self.carddb[int(card.master_card_id)][1])
            card.lv_i=int(card.lv)
            card.hp_i=int(card.hp)
            card.atk_i=int(card.power)
            card.mid=int(card.master_card_id)
            card.price=int(card.sale_price)
            card.sid=int(card.serial_id)
            evalres=eval(self.evalstr_selcard) and not card.mid in [390,391,392]#切尔莉
            if evalres:
                if card.star>3:
                    warning_card.append(self.carddb[int(card.master_card_id)][0]+
                        du8(' lv%d ☆%s'%(card.lv_i,self.carddb[int(card.master_card_id)][1])))
                sid.append(card.serial_id)
                cinfo.append(self.carddb[int(card.master_card_id)][0]+
                    du8(' lv%d ☆%s'%(card.lv_i,self.carddb[int(card.master_card_id)][1])))
        logging.info(len(sid)==0 and du8('没有要贩卖的卡片') or du8('将要贩卖这些卡片：')+', '.join(cinfo))
        if len(warning_card)>0:
            if self.cfg_sell_card_warning>=1:
                logging.warning(du8('存在稀有以上卡片：')+', '.join(warning_card)+'\n真的要继续吗？y/n')
                if raw_input('> ')=='y':
                    self._sell_card(sid)
                else:
                    logging.debug('select_card:user aborted')
            else:
                    logging.debug('select_card:auto aborted')
        else:
            if self.cfg_sell_card_warning==2:
                logging.warning(du8('根据卖卡警告设置，需要亚瑟大人的确认\n真的要继续吗？y/n'))
                if raw_input('> ')=='y':
                    self._sell_card(sid)
                else:
                    logging.debug('select_card:user aborted')
            else:
               self._sell_card(sid)

    def _sell_card(self,serial_id):
        if serial_id==[]:
            logging.debug('sell_card:no cards selected')
            return
        if self._dopost('card/exchange',postdata='mode=1')[0]['error']:
            return 0
        while len(serial_id)>0:
            #>30张要分割
            if len(serial_id)>30:
                logging.debug('_sell_card:too many cards (%d)'%(len(serial_id)))
                se_id=serial_id[:30]
            else:
                se_id=serial_id
            serial_id=serial_id[len(se_id):]
            #卖
            paramsell='serial_id=%s'%(','.join(se_id))
            slp=random.random()*15+7
            logging.inform(du8('%f秒后卖卡……'%slp))
            time.sleep(slp)
            resp,ct=self._dopost('trunk/sell',postdata=paramsell)
            if not resp['error']:
                logging.info(resp['errmsg']+du8('(%d张卡片)'%len(se_id)))


    def fairy_battle_loop(self,ltime=None):
        if ltime!=None and ltime!='':
            looptime=ltime
        else:
            looptime=self._read_config('system','fairy_battle_times')
        if looptime=='0' or looptime=='':
            looptime='9999999'
        looptime=int(looptime)
        slptime=self._read_config('system','fairy_battle_sleep')
        slpfactor=float(self._read_config('system','fairy_battle_sleep_factor') or '1')
        if slptime=='':
            slptime=1.5
        secs=slptime.split('|')
        hour_last=99999
        for l in xrange(looptime):
            hour_now=int(time.strftime('%H',time.localtime(time.time())))
            if hour_now!=hour_last:
                for s in secs:
                    low,up,t=s.split(',')
                    if hour_now in xrange(int(low),int(up)):
                        slptime=float(t)
                        break
                    slptime=1.5
                hour_last=hour_now
            logging.debug('fairy_battle_loop:%d/%d'%(l+1,looptime))
            refresh=self.fairy_select()
            if not refresh:#没有立即刷新
                s=random.randint(int(60*slptime*0.8*slpfactor),int(60*slptime*1.2*slpfactor))
                logging.inform(du8('%d秒后刷新……'%s))
                time.sleep(s)



    def fairy_select(self,cond=''):
        resp,ct=self._dopost('menu/menulist')
        if resp['error']:
            return
        time.sleep(2)
        resp,ct=self._dopost('mainmenu')
        if resp['error']:
            return
        if XML2Dict().fromstring(ct).response.header.your_data.fairy_appearance!='1':
            return
        time.sleep(2)
        resp,ct=self._dopost('menu/fairyselect')
        if resp['error']:
            return
        fs=XML2Dict().fromstring(ct).response.body.fairy_select
        fairy_event=fs.fairy_event
        if fs.remaining_rewards!='0':
            if self.cfg_auto_fairy_rewards:
                self._fairy_rewards()
            else:
                logging.debug('fairy_select:do not get rewards')
        else:
            logging.debug('fairy_select:no rewards')
        #清理记录
        fsids=[f.fairy.serial_id for f in fairy_event]
        for fsid in self._list_option('fairy'):
            if int(self._read_config('fairy',fsid).split(',')[0])<time.time() or not fsid in fsids:
                logging.debug('fairy_select:delete sid %s from record'%(fsid))
                self._del_option('fairy',fsid)
        #筛选
        fitemp= self.player.fairy['id']
        self.player.fairy={'alive':False,'id':0}
        evalstr=(cond!='' and self._eval_gen(cond) or self.evalstr_fairy)
        logging.debug('fairy_select:eval:%s'%(evalstr))
        fairies=[]
        for fairy in fairy_event:
            fairy.fairy.lv=int(fairy.fairy.lv)
             #检查自己的还活着不
            if fitemp==fairy.fairy.serial_id and fairy.put_down=='1':
                self.player.fairy={'alive':True,'id':fairy.fairy.serial_id}
            fairy['time_limit']=int(fairy.fairy.time_limit)
            fairy['wake']=fairy.fairy.name[:2] in ['觉醒','覺醒','希波','數理','教官','雅熙']
            ftime=(self._read_config('fairy',fairy.fairy.serial_id)+',,').split(',')
            fairy['not_battled']= ftime[0]==''
            #logging.debug('b%s e%s p%s'%(not fairy['not_battled'],eval(evalstr),fairy.put_down))
            if eval(evalstr):
                if time.time()-int(ftime[1] or '0') < 180:
                    logging.debug('fairy_select:sid %s battled in less than 3 min'%fairy.fairy.serial_id)
                    continue
                fairies.append(fairy)
        logging.info(du8(len(fairies)==0 and '木有符合条件的妖精-v-' or '符合条件的有%d只妖精XD'%len(fairies)))
        instant_refresh=False
        for f in fairies:
            logging.debug('fairy_select:select sid %s discoverer %s battled %s'%(f.fairy.serial_id,f.user.name,not f.not_battled))
            f.fairy.discoverer_id=f.user.id
            if self._fairy_battle(f.fairy,type=NORMAL_BATTLE):
                instant_refresh=True
            #走个形式
            resp,ct=self._dopost('menu/fairyselect')
            if resp['error']:
                return
        return instant_refresh
            #fairy.user.name,fairy.fairy.name,fairy.fairy.serial_id,fairy.fairy.lv,fairy.put_down
            #fairy.start_time,fairy.fairy.time_limit
    def _fairy_rewards(self):
        resp,ct=self._dopost('menu/fairyrewards')
        if resp['error']:
            return
        rws=XML2Dict().fromstring(ct).response.body.fairy_rewards.reward_details
        if 'fairy' in rws:
            rws=[rws]
        rwname=[]
        for rw in rws:
            rwname.append(rw.item_name)
        logging.info(', '.join(rwname)+du8('  已获得'))

    def _fairy_battle(self,fairy,type=NORMAL_BATTLE):
        '''
        Return bool 是否需要立即重刷列表
        '''
        def fairy_floor():
            paramfl='check=1&serial_id=%s&user_id=%s'%(fairy.serial_id,fairy.discoverer_id)
            resp,ct=self._dopost('exploration/fairy_floor',postdata=paramfl)
            return XML2Dict().fromstring(ct).response.body.fairy_floor.explore.fairy
        if type==NORMAL_BATTLE:    
            fairy=fairy_floor()#走形式
        fairy['lv']=int(fairy.lv)
        fairy['hp']=int(fairy.hp)
        fairy['time_limit']=int(fairy.time_limit)
        if not 'attacker' in fairy.attacker_history:
            fairy.attacker_history.attacker=[]
        if fairy.attacker_history.attacker==[]:
            disc_name=self.player.name
        else:
            #只有一个的情况
            if 'user_id' in fairy.attacker_history.attacker:
                fairy.attacker_history.attacker=[fairy.attacker_history.attacker]
            for atk in fairy.attacker_history.attacker:
                if atk.discoverer=='1':
                    disc_name=atk.user_name
                    break
        hms=lambda x:x>=3600 and time.strftime('%H:%M:%S',time.localtime(x+16*3600)) or time.strftime('%M:%S',time.localtime(x))
        logging.info('%s:%sLv%d hp:%d %s:%s %s:%d %s%s %s'%(
            du8('妖精'),fairy.name,fairy.lv,fairy.hp,du8('发现者'),disc_name,
            du8('小伙伴'),len(fairy.attacker_history.attacker),du8('剩余'),hms(fairy.time_limit),
            fairy.rare_flg=='1' and 'WAKE!' or''))
        cardd=eval(self.evalstr_fairy_select_carddeck)
        logging.debug('fairy_battle:eval:%s result:%s'%(self.evalstr_fairy_select_carddeck,cardd))
        if (self.set_card(cardd)):
            fairy=fairy_floor()#设完卡组返回时
        #打
        if self.check_strict_bc():#strict BC
            logging.warning(du8('BC不够了TOT'))
            autored=(self.cfg_auto_rt_level=='2') or (self.cfg_auto_rt_level=='1' and fairy.rare_flg=='1')
            if not self.red_tea(autored):
                logging.error(du8('那就不打了哟(*￣︶￣)y '))
                return False
            else:
                return True
        paramf='serial_id=%s&user_id=%s'%(fairy.serial_id,fairy.discoverer_id)
        resp,ct=self._dopost('exploration/fairybattle',postdata=paramf)
        if resp['error']:
            return
        elif resp['errno']==1050:
            logging.warning(du8('BC不够了TOT'))
            autored=(self.cfg_auto_rt_level=='2') or (self.cfg_auto_rt_level=='1' and fairy.rare_flg=='1')
            if not self.red_tea(autored):
                logging.error(du8('那就不打了哟(*￣︶￣)y '))
                return False
            else:
                return True
        try:
            res=XML2Dict().fromstring(ct).response.body.battle_result
        except KeyError:
            logging.warning(du8('没有发现奖励，妖精已经挂了？'))
            return False
        self.remoteHdl(method='FAIRY',fairy=fairy)
        need_refresh=False
        if res.winner=='1':#赢了
            logging.info(du8('YOU WIN 233'))
            bonus=XML2Dict().fromstring(ct).response.body.bonus_list.bonus
            nid=[]
            for b in bonus:
                if 'item_id' in b:
                    #logging.debug('fairy_battle:type:%s item_id %s count %s'%(b.type,b.item_id,b.item_num))
                    logging.info(du8('获得收集品[')+self.itemdb[int(b.item_id)]+'] x'+b.item_num)
                    nid.append(b.id)
                else:
                    logging.debug('fairy_battle:type:%s card_id %s holoflag %s'%(b.type,b.card_id,b.holo_flag))
                    logging.info(du8('获得卡片 ')+self.carddb[int(b.card_id)][0]+(b.holo_flag=='1' and du8('(闪)') or ''))
            if nid!=[]:
                res=elf._get_rewards(nid)
                if not res[0]:
                    logging.warning(res[1])
            if fairy.serial_id==self.player.fairy['id']:
                self.player.fairy={'id':0,'alive':False}
        else:
            hpleft=int(XML2Dict().fromstring(ct).response.body.explore.fairy.hp)
            logging.info(du8('YOU LOSE- - Fairy-HP:%d'%hpleft))
            if self.cfg_fairy_final_kill_hp>=hpleft:
                logging.debug('_fairy_battle:instant refresh!')
                need_refresh=True
        logging.info(du8('EXP:+%d(%s) G:+%d(%s)'%(
            int(res.before_exp)-int(res.after_exp),
            res.after_exp,
            int(res.after_gold)-int(res.before_gold),
            res.after_gold
        )))
            
        if not res.before_level==res.after_level:
            logging.info(du8('升级了：↑%s'%res.after_level))
        if 'special_item' in res:
            it=res.special_item
            logging.info(du8('收集品[%s]:+%d(%s)'%(\
                self.itemdb[int(it.item_id)],int(it.after_count)-int(it.before_count),it.after_count)))
        if not need_refresh:
            #等着看结果
            time.sleep(4)
        #记录截止时间，上次战斗时间，如果需要立即刷新，上次战斗时间为0.1
        self._write_config('fairy',fairy.serial_id,
            '%d,%.0f'%(int(fairy.time_limit)+int(float(time.time())),need_refresh and 0.1 or time.time()))
        return need_refresh

    def friends(self,choice='',autodel=False):
        delfriend=int(self._read_config('system','del_friend_day') or '5')
        loop=999
        lastmove=0
        while loop-1>0:
            loop-=1
            if choice=='':
                print(du8('选择操作\n1.删除好友\n2.查找添加好友\n3.处理好友邀请\n4.返回'))
                choice= raw_input('> ')
            else:
                loop=1
            if choice=='1':
                resp,dec=self._dopost('menu/friendlist',postdata='move=0')
                lastmove=1
                if resp['error']:
                    return
                try:
                    users=XML2Dict().fromstring(dec).response.body.friend_list.user
                except KeyError:
                    users=[]
                else:
                    if 'name' in users:
                        users=[users]
                strf=du8('已有好友个数：%d\n'%len(users))
                i=1
                deluser=None
                maxlogintime=0
                for user in users:
                    strf+='%d.%s\t最后上线:%s  LV:%s  BC:%s\n'%(
                        i,user.name,user.last_login,user.town_level,user.cost
                    )
                    try:
                        user.logintime=int(user.last_login[:-1])
                    except UnicodeEncodeError:
                        if user.last_login.endswith('月前'):
                            user.logintime=31
                        else :
                            user.logintime=0
                    if user.logintime>delfriend and user.logintime>maxlogintime:
                        deluser=user
                        maxlogintime=user.logintime
                    i+=1
                logging.info(strf)
                if deluser!=None:
                    doit=False
                    if not autodel:
                        logging.warning(du8('即将删除%d天以上没上线的：'%delfriend)+'%s 最后上线:%s ID:%s'%(
                            deluser.name,deluser.last_login,deluser.id
                        ))
                        if self._raw_input('y/n >')=='y':
                            doit=True
                    if autodel or doit:
                        param='dialog=1&user_id=%s'%deluser.id
                        resp,dec=self._dopost('friend/remove_friend',postdata=param)
                        logging.info(resp['errmsg'])
                else:
                    logging.debug(du8('没有要删除的好友'))
            elif choice=='3':
                lastmove=3
                resp,dec=self._dopost('menu/friend_notice',postdata='move=0')
                if resp['error']:return
                try:
                    users=XML2Dict().fromstring(dec).response.body.friend_notice.user_list.user
                except KeyError:
                    users=[]
                else:
                    if 'name' in users:
                        users=[users]
                i=1
                strf=''
                for user in users:
                    strf+='%d.%s\tLV:%s\t最后上线:%s\t好友:%s/%s\tBC:%s\n'%(
                        i,user.name,user.town_level,user.last_login,user.friends,user.friend_max,user.cost
                    )
                    i+=1
                logging.info(du8('申请列表:\n')+strf)
                adduser=self._raw_input('选择要添加的好友序号，空格分割，序号前加减号表示拒绝> ').split(' ')
                if adduser!=['']:
                    for u in adduser:
                        if u.startswith('-'):
                            u=u[1:]
                            param='dialog=1&user_id=%s'%users[int(u)-1].id
                            resp,dec=self._dopost('friend/refuse_friend',postdata=param)
                        else:
                            if users[int(u)-1].friends==users[int(u)-1].friend_max:
                                logging.warning(du8('无法成为好友ww'))
                            param='dialog=1&user_id=%s'%users[int(u)-1].id
                            resp,dec=self._dopost('friend/approve_friend',postdata=param)
                        logging.info(resp['errmsg'])
                        time.sleep(2)
            elif choice=='2':
                if lastmove!=2:
                    resp,dec=self._dopost('menu/other_list')
                lastmove=2
                qry=self._raw_input('输入关键词> ').decode(locale.getdefaultlocale()[1] or 'utf-8').encode('utf-8')
                param='name=%s'%qry
                resp,dec=self._dopost('menu/player_search',postdata=param)
                if resp['error']:return
                try:
                    users=XML2Dict().fromstring(dec).response.body.player_search.user_list.user
                except:
                    users=[]
                else:
                    if 'name' in users:
                        users=[users]
                i=1
                strf=''
                for user in users:
                    strf+='%d.%s\tLV:%s\t最后上线:%s\t好友:%s/%s\tBC:%s\n'%(
                        i,user.name,user.town_level,user.last_login,user.friends,user.friend_max,user.cost
                    )
                    i+=1
                logging.info(du8('搜索结果:\n')+strf)
                u=self._raw_input('选择要添加的好友序号> ')
                if u!='':
                    if users[int(u)-1].friends==users[int(u)-1].friend_max:
                        logging.warning(du8('无法成为好友ww'))
                    param='dialog=1&user_id=%s'%users[int(u)-1].id
                    resp,dec=self._dopost('friend/approve_friend',postdata=param)
                    logging.info(resp['errmsg'])
            elif choice=='4':
                return True
            else:
                logging.error(du8('木有这个选项哟0w0'))
            choice=''

    def reward_box(self):
        if self._dopost('menu/menulist')[0]['error']:
            return False
        resp,ct=self._dopost('mainmenu')
        if resp['error']:
            return False
        if XML2Dict().fromstring(ct).response.body.mainmenu.rewards=='0':
            logging.info(du8('木有礼物盒wwww'))
            return False
        resp,ct=self._dopost('menu/rewardbox')
        if resp['error']:
            return False
        rwds=XML2Dict().fromstring(ct).response.body.rewardbox_list.rewardbox
        if 'id' in rwds:
            rwds=[rwds]
        strl=''
        nid=[]
        #type 2:道具 3:4:绊点 金 5:蛋卷 1:卡片
        for r in rwds:
            strl+=('%s:'%r.content)
            if r.type=='1':
                strl+='%s'%(self.carddb[int(r.card_id)][0])
            elif r.type=='2':
                strl+='%sx%s'%(self.itemdb[int(r.item_id)],r.get_num)
            elif r.type=='3':
                strl+='%sG'%r.point
            elif r.type=='4':
                strl+='%sFP'%r.point
            elif r.type=='5':
                strl+='%sx%s'%(du8('蛋蛋卷'),r.get_num)
            else:
                strl+=r.type
            strl+=', '
            nid.append(r.id)
        logging.info(strl.rstrip(','))
        res=self._get_rewards(nid)
        if res[0]:
            logging.info(res[1])


    def point_setting(self):
        if self._dopost('menu/playerinfo',postdata='kind=6&user_id=%s'%self.player.id)[0]['error']:
            return
        resp,ct=self._dopost('town/lvup_status',postdata='kind=6&user_id=%s'%self.player.id)
        if resp['error']:
            return
        free_points = int(XML2Dict().fromstring(ct).response.header.your_data.free_ap_bc_point)
        if free_points==0:
            logging.info(du8('没有未分配点数233'))
            return False
        else:
            logging.info(du8('还有%d点未分配点数'%free_points))
        while True:
            try:
                ap,bc=self._raw_input('输入要分配给AP BC的点数，空格分隔> ').split(' ')
            except ValueError:
                logging.warning(du8('少输入了一个数或者多输了一个数吧'))
            else:
                break
        if not self._dopost('town/pointsetting',postdata='ap=%s&bc=%s'%(ap,bc))[0]['error']:
            logging.info(du8('点数分配成功！'))
            return True


    def factor_battle(self,minbc=0):
        minbc=int(minbc)
        self._dopost('battle/area',checkerror=False)
        resp,dec=self._dopost('battle/competition_parts?redirect_flg=1',noencrypt=True)
        if resp['error']:
            return 
        lakes=XML2Dict().fromstring(dec).response.body.competition_parts.lake
        #only one
        if len(lakes)==1:
            lakes=[lakes]
        #try count
        trycnt=self._read_config('system','try_factor_times')
        if trycnt=='0':
            trycnt='999'
        #try loop
        for i in xrange(int(trycnt)):
            logging.debug(du8('factor_battle:因子战:第%d/%s次 寻找油腻的师姐'%(i+1,trycnt)))
            l=random.choice(lakes)
            if l.lake_id=='0':
                partids=[0]
            else:
                partids=[i for i in xrange(1,10)]
            random.shuffle(partids)
            #circulate part id
            for partid in partids:
                if self.player.bc['current']<=minbc:
                    logging.info(du8('BC已突破下限%d，退出o(*≧▽≦)ツ '%minbc))
                    return
                logging.info(du8('选择因子 %s:%s, 碎片id %d'%(l.lake_id,l.lake_id=='0' and 'NONE' or l.title,partid)))
                param='knight_id=%s&move=1&parts_id=%d'%(l.lake_id,partid)
                resp,dec=self._dopost('battle/battle_userlist',postdata=param)
                if resp['error']:
                    continue
                #print xml2.response.body.battle/battle_userlist.user_list
                try:
                    userlist=XML2Dict().fromstring(dec).response.body.battle_userlist.user_list.user
                except KeyError:#no user found
                    continue
                if len(userlist)==18:#only 1 user
                    userlist=[userlist]
                for u in userlist:
                    cid=int(u.leader_card.master_card_id)
                    try:
                        star=int(self.carddb[cid][1])
                    except KeyError:
                        logging.warning(du8('id为 %d 的卡片木有找到. 你可能想要查看这个网页:\n%s'%(
                            cid,
                            duowan[self.loc[:2]]%(base64.encodestring('{"no":"%d"}'%cid).strip('\n').replace('=','_3_')))))
                    else:
                        logging.debug('factor_battle:eval:%s, result:%s, star:%s, cid:%d'%(
                            evalstr,
                            eval(self.evalstr_factor),
                            star,
                            cid)
                        )
                        if eval(self.evalstr_factor):
                            logging.debug('factor_battle:->%s @ %s'%(u.name,u.leader_card.master_card_id))
                            ap=self.player.ap['current']
                            bc=self.player.bc['current']
                            logging.info('%s%s%s'%(du8('艹了一下一个叫 '),u.name,du8(' 的家伙')))
                            fparam='lake_id=%s&parts_id=%d&user_id=%s'%(l.lake_id,partid,u.id)
                            resp,dec=self._dopost('battle/battle',postdata=fparam)
                            if resp['error']:
                                continue
                            elif resp['errno']==1050:
                                logging.warning(du8('BC不够了TOT'))
                                if not self.red_tea(False):
                                    logging.error(du8('那就不打了哟(*￣︶￣)y '))
                                    return
                            else:
                                try:
                                    result=XML2Dict().fromstring(dec).response.body.battle_result.winner
                                except KeyError:
                                    logging.warning('no BC ?')
                                    return
                                #print bc,self.player.bc.current
                                logging.info(du8(result=='0' and '擦输了QAQ' or '赢了XDDD')+
                                    ' AP:%s%d/%s/%s'%(
                                        self.player.ap['current']>=ap and '+' or '',
                                        self.player.ap['current']-ap,
                                        self.player.ap['current'],
                                        self.player.ap['max'])+
                                    ' BC:%s%d/%s/%s'%(
                                        self.player.bc['current']>=bc and '+' or '',
                                        self.player.bc['current']-bc,
                                        self.player.bc['current'],
                                        self.player.bc['max']) )
                                time.sleep(8.62616513)
                                self._dopost('battle/area',checkerror=False)
                                resp,dec=self._dopost('battle/competition_parts?redirect_flg=1',noencrypt=True)
                                break
                time.sleep(int(self._read_config('system','factor_sleep')))
            logging.inform(du8('换一个碎片……睡觉先，勿扰：-/'))
            time.sleep(int(self._read_config('system','factor_sleep')))

    def remote_Hdl_(self):
        def do(method=None,fairy=''):
            if method==None:
                informed=False
                while True:
                    #print(self.remote.status,self.remote.STARTED)
                    if self.remote.status==self.remote.STARTED:
                        if self.remote.tasker!='':
                            self.tasker(cmd=self.remote.get_task())
                        break
                    if not informed:
                        logging.inform(du8('remote_hdl:已被远程停止，等待开始信号ww'))
                        informed=True
                    time.sleep(30)
            elif method=='PROFILE':
                self.remote.set(
                    {'ap_current':self.player.ap['current'],
                    'ap_max':self.player.ap['max'],
                    'bc_current':self.player.bc['current'],
                    'bc_max':self.player.bc['max'],
                    'gold':self.player.gold})
            elif method=='FAIRY':
                self.remote.fckfairy(fairy)
            if self.remote.lastprofile!=0:
                logging.debug('remote_hdl:profile has been uploaded %s seconds ago'%
                    (int(time.time()-self.remote.lastprofile)))
                self.remote.lastprofile=0
        return do

    def _exit(self,code=0):
        # if self.settitle:
        #     self.stitle.flag=0
        #     self.stitle.join(0.1)
        raw_input('THAT\'S THE END')
        sys.exit(code)

    def download_card(self,cardid,level=CARD_NORM):
        #print serv['%s_data'%self.loc]+uri['%s_data_card'%loc]+uri['cardlevel'][level]%cardid
        rev={'cn_card':169,'tw_card':171}
        card={'cn_data_card':'MA/PROD/%d/'%rev['cn_card'],'tw_data_card':'contents/%d/'%rev['tw_card'],\
        'cardlevel':\
            ['card_full/full_thumbnail_chara_%d?cyt=1','card_full_max/full_thumbnail_chara_5%03d?cyt=1',\
            'card_full_h/full_thumbnail_chara_%d_horo?cyt=1','card_full_h_max/full_thumbnail_chara_5%03d_horo?cyt=1']
        }
        resp,content=ht.request(serv['%s_data'%self.loc]+card['%s_data_card'%self.loc]+card['cardlevel'][level]%cardid,\
                method='GET',headers={'ua':'Million/100','accept':'gzip','connection':'keep-alive'})
        return content


if __name__=='__main__':
    '''cardid=int(raw_input('cardid > '))
    level=raw_input('level > ')
    for j in level.split(','):
        dt=ma.decode_res(download_card(cardid,int(j),'tw'))
        open('Z:\\%d_%s.png'%(cardid,j),'wb').write(dt)'''
    if len(sys.argv)>=2:
        maClient1=maClient(configfile=sys.argv[1],savesession=True)
    else:
        maClient1=maClient(savesession=True)
    #进入游戏
    #maClient1._dopost('notification/post_devicetoken',postdata=ma.encode_param('S=nosessionid&login_id=%s&password=%s&app=and&token=BubYIgiyDYTFUifydHIoIOGBiujgRzrEFUIbIKOHniHIoihoiHasbdhasbdUIUBujhbjhjBJKJBb'%(username,password)),extraheader={'Cookie2': '$Version=1'})
    #登陆
    #import profile
    #profile.run("maClient1.login()")
    os._exit(0)
    maClient1.login()
    dec=maClient1.login()
    maClient1.initplayer(dec)
    #maClient1._gacha(gacha_type=GACHA_FRIENNSHIP_POINT)
    #maClient1._sell_card(['59775010'])
    #maClient1.tasker()
    #maClient1.explore()
    #maClient1.set_card('factor')
    #maClient1.factor_battle()
    #妖精列表
    #maClient1._dopost('menu_fairy_sel')
    #maClient1.set_card(['124'])
    #exploration/fairy_floor，check=HJQrxs%2FKaF3hyO81WS2jdA%3D%3D%0A&serial_id=W0etULbphY0EqnmoIG2Zcg%3D%3D%0A&user_id=r%2BFl%2BYcd4QrirAFwiDWIRw%3D%3D%0A
    #exploration/fairybattle,serial_id=W0etULbphY0EqnmoIG2Zcg%3D%3D%0A&user_id=r%2BFl%2BYcd4QrirAFwiDWIRw%3D%3D%0A

    #exploration/area
    #exploration/floor,area_id=Q5E9%2FUAjnkmbZhPSCR6nnw%3D%3D%0A
    #exploration/get_floor，area_id=Q5E9%2FUAjnkmbZhPSCR6nnw%3D%3D%0A&check=HJQrxs%2FKaF3hyO81WS2jdA%3D%3D%0A&floor_id=3sJ7qONwz5JawDpnsoUDJQ%3D%3D%0A
    #exploration/explore，area_id=Q5E9%2FUAjnkmbZhPSCR6nnw%3D%3D%0A&auto_build=HJQrxs%2FKaF3hyO81WS2jdA%3D%3D%0A&floor_id=3sJ7qONwz5JawDpnsoUDJQ%3D%3D%0A

    #roundtable/edit，move=HJQrxs%2FKaF3hyO81WS2jdA%3D%3D%0A 返回？
    #app/cardselect/savedeckcard，C=%2BRsca9Zy2x8L1yprbkM494x7rw%2B0vUKp%2Fpc%2BN%2B2sFH3zGeMHnPJkwThx3cDEbfVXEAjoR9k2p7EF%0A6D31AT9oQ2PWUTs9pdB0p4%2FNZmMBHEQ%3D%0A&lr=9ZeY%2BCMCjZpBgiMOHfyTRg%3D%3D%0A