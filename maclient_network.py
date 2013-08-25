#coding:utf-8
import os
import base64
import socket
import urllib
import httplib
import httplib2
from Crypto.Cipher import AES
key={'res': '?'*16,'helper':'?'*16,'crypt':'?'*16}

serv={'cn':'http://game1-CBT.ma.sdo.com:10001/connect/app/','cn_data':'http://MA.webpatch.sdg-china.com/',
    'cn2':'http://game2-CBT.ma.sdo.com:10001/connect/app/','cn2_data':'http://MA.webpatch.sdg-china.com/',
    'tw':'http://game.ma.mobimon.com.tw:10001/connect/app/','tw_data':'http://download.ma.mobimon.com.tw/'
    }

uri={'check_inspection':'check_inspection?cyt=1','post_token':'notification/post_devicetoken?cyt=1','login':'login?cyt=1',
    'edit_card':'roundtable/edit?cyt=1','set_card':'cardselect/savedeckcard?cyt=1',
    'battle_init':'battle/area?cyt=1','battle_parts':'battle/competition_parts?redirect_flg=1','battle_userlist':'battle/battle_userlist?cyt=1','battle':'battle/battle?cyt=1',
    'explore_area':'exploration/area?cyt=1','explore_floor':'exploration/floor?cyt=1','explore_get_floor':'exploration/get_floor?cyt=1','explore':'exploration/explore?cyt=1',
    'explore_battle':'exploration/fairybattle?cyt=1','explore_battle_lose':'exploration/fairy_lose?cyt=1','explore_fairy_floor':'exploration/fairy_floor?cyt=1',
    'fairy_rewards':'menu/fairyrewards?cyt=1',
    'card_exchange':'card/exchange?cyt=1','trunk_sell':'trunk/sell?cyt=1',
    'gacha_select':'gacha/select/getcontents?cyt=1','gacha_buy':'gacha/buy?cyt=1',
    'item_use':'item/use?cyt=1',
    'menu_friend_notice':'menu/friend_notice?cyt=1','menu_friendlist':'menu/friendlist?cyt=1','remove_friend':'friend/remove_friend?cyt=1','approve_friend':'friend/approve_friend?cyt=1','refuse_friend':'friend/refuse_friend?cyt=1','friend_other':'menu/other_list?cyt=1','player_search':'menu/player_search?cyt=1',
    'main_menu':'mainmenu?cyt=1','menu_fairy_select':'menu/fairyselect?cyt=1','menu_get_rewards':'menu/get_rewards?cyt=1','menu_fairy_rewards':'menu/fairyrewards?cyt=1','menu_list':'menu/menulist?cyt=1',
    }
headers_main={'User-Agent': 'Million/100 (GT-I9100; GT-I9100; 2.3.4) samsung/GT-I9100/GT-I9100:2.3.4/GRJ22/eng.build.20120314.185218:eng/release-keys','Connection': 'Keep-Alive'}
headers_post={'Content-Type': 'application/x-www-form-urlencoded'}
cod_res = AES.new(key['res'], AES.MODE_ECB)
cod_data = AES.new(key['crypt'], AES.MODE_ECB)
BS=16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1])]
ht=httplib2.Http(timeout=15)
def decode_res(bytein):
    return cod_res.decrypt(bytein)

def decode_data(bytein):
    if len(bytein)==0:
        return ''
    else:
        return unpad(cod_data.decrypt(bytein))

def decode_data64(strin):
    return decode_data(base64.decodestring(urlescape(strin)))

def encode_data(bytein):
    return cod_data.encrypt(pad(bytein))

def encode_data64(bytein):
    return urlunescape(base64.encodestring(encode_data(bytein)).strip('\n'))

def encode_param(param):
    p=param.split('&')
    p_enc='%0A&'.join([p[i].split('=')[0]+'='+encode_data64(p[i].split('=')[1]) for i in xrange(len(p))])
    #print p_enc
    return p_enc.replace('\n','')

def decode_param(param_enc):
    p_enc=param_enc.split('&')
    p='%0A&'.join([p_enc[i].split('=')[0]+'='+decode_data64(p_enc[i].split('=')[1]) for i in xrange(len(p_enc))])
    return p

def urlunescape(url):
    return url.replace('=','%3D').replace('&','%0A').replace('/','%2F').replace('+','%2B')

def urlescape(url):
    return url.replace('%3D','=').replace('%0A','&').replace('%2F','/').replace('%2B','+')

def decrypt_file(filein,fileout,ext='png'):
    fileout='%s.%s'%(fileout,ext)
    if not os.path.exists(os.path.split(fileout)[0]):
        os.makedirs(os.path.split(fileout)[0])
    try:
        if not os.path.exists(fileout):
            open(fileout,'wb').write(decode_res(open(filein,'rb').read()))
    except ValueError:
        print('skip',filein)
    else:
        pass
class poster():
    def __init__(self,mac,loc,logger,ua):
        self.cookie=''
        self.maClientInstance=mac
        self.servloc=loc
        self.logger=logger
        self.header=headers_main
        self.header.update(headers_post)
        self.header['User-Agent']=ua
    def set_cookie(self,cookie):
        self.cookie=cookie
    def post(self,urikey,postdata='',usecookie=True,setcookie=True,extraheader={'Cookie2': '$Version=1'},noencrypt=False):
            header={}
            header.update(self.header)
            header.update(extraheader)
            if usecookie:
                header.update({'Cookie':self.cookie})
            if not noencrypt and postdata!='':
                postdata=encode_param(postdata)
            trytime=0
            ttimes=3
            while trytime<ttimes:
                try:
                    resp,content=ht.request(serv[self.servloc]+uri[urikey],method='POST',headers=header,body=postdata)
                except socket.error,e:
                    if e.errno==None:
                        err='Timed out'
                    else:
                        err=e.errno
                    self.logger.warning('post:%s got socket error:%s, retrying in %d times'%(urikey,err,ttimes-trytime))
                except httplib.ResponseNotReady:
                    self.logger.warning('post:socket closed, retrying in %d times'%(ttimes-trytime))
                except httplib2.ServerNotFoundError:
                    self.logger.warning('post:no internet, retrying in %d times'%(ttimes-trytime))
                else:
                    if int(resp['status'])<400:
                        break
                    time.sleep(2.818281828)
                    self.logger.warning('post:POSTing %s, server returns code %s, retrying in %d times'%(urikey,resp['status'],3-trytime))
                resp,content={'status':'600'},''
                trytime+=1
            dec=decode_data(content)
            if os.path.exists('debug'):
                open('debug/'+urikey+'.xml','w').write(dec)
            
            if not 'content-length' in resp:
                resp['content-length']=str(len(dec))
            if int(resp['status'])>400:
                self.logger.error('post:'+urikey+'-'+','.join([ ( i in resp and (i+':'+resp[i]) or '' )for i in ['status','content-length','set-cookie']])+du8('\n请到信号良好的地方重试【←←'))
                resp.update({'error':True,'errno':resp['status'],'errmsg':'Client or server error.'})
                return resp,dec
            else:
                self.logger.debug('post:'+urikey+'-'+','.join([ ( i in resp and (i+':'+resp[i]) or '' )for i in ['status','content-length','set-cookie']]))
            if setcookie and 'set-cookie' in resp:
                self.cookie=resp['set-cookie'].split(',')[-1].rstrip('path=/').strip()
            #print self.cookie
            return resp,dec