#!/usr/bin/env python
# coding:utf-8
# maclient network utility
# Contributor:
#      fffonion        <fffonion@gmail.com>
import os
import time
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

headers_main={'User-Agent': 'Million/100 (GT-I9100; GT-I9100; 2.3.4) samsung/GT-I9100/GT-I9100:2.3.4/GRJ22/eng.build.20120314.185218:eng/release-keys','Connection': 'Keep-Alive'}
headers_post={'Content-Type': 'application/x-www-form-urlencoded'}
cod_res = AES.new(key['res'], AES.MODE_ECB)
cod_data = AES.new(key['crypt'], AES.MODE_ECB)
BS=16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1])]
du8=lambda str:str.decode('utf-8')
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
        if ua:
            self.header['User-Agent']=ua
    def set_cookie(self,cookie):
        self.cookie=cookie
    def post(self,uri,postdata='',usecookie=True,setcookie=True,extraheader={'Cookie2': '$Version=1'},noencrypt=False):
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
                    resp,content=ht.request('%s%s%s'%(serv[self.servloc],uri,not noencrypt and '?cyt=1' or ''),method='POST',headers=header,body=postdata)
                except socket.error,e:
                    if e.errno==None:
                        err='Timed out'
                    else:
                        err=e.errno
                    self.logger.warning('post:%s got socket error:%s, retrying in %d times'%(uri,err,ttimes-trytime))
                except httplib.ResponseNotReady:
                    self.logger.warning('post:socket closed, retrying in %d times'%(ttimes-trytime))
                except httplib2.ServerNotFoundError:
                    self.logger.warning('post:no internet, retrying in %d times'%(ttimes-trytime))
                else:
                    if int(resp['status'])<400:
                        break
                    time.sleep(2.718281828)
                    self.logger.warning('post:POSTing %s, server returns code %s, retrying in %d times'%(uri,resp['status'],3-trytime))
                resp,content={'status':'600'},''
                trytime+=1
            dec=decode_data(content)
            if os.path.exists('debug'):
                open('debug/%s.xml'%uri.replace('/','#').replace('?','~'),'w').write(dec)
            
            if not 'content-length' in resp:
                resp['content-length']=str(len(dec))
            if int(resp['status'])>400:
                self.logger.error('post:%s %s'%(uri,','.join([ ( i in resp and (i+':'+resp[i]) or '' )for i in ['status','content-length','set-cookie']])+du8('\n请到信号良好的地方重试【←←')))
                resp.update({'error':True,'errno':resp['status'],'errmsg':'Client or server error.'})
                return resp,dec
            else:
                self.logger.debug('post:%s %s'%(uri,','.join([ ( i in resp and (i+':'+resp[i]) or '' )for i in ['status','content-length','set-cookie']])))
            if setcookie and 'set-cookie' in resp:
                self.cookie=resp['set-cookie'].split(',')[-1].rstrip('path=/').strip()
            #print self.cookie
            return resp,dec

if __name__=="__main__":
    print decode_param('notice_id=yYR9MXvxbQ3ZCzjF89B%2FG3HG%2Fho0AoGJbzYwu6SJ5GR0Mm6xGffIWvXmPsOBGJrn7Gjjp2rkAdG3%0ANLHJZ6tgqw%3D%3D%0A')