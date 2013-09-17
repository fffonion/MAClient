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
try:
    import httplib
except ImportError:
    import http.client as httplib
try:
    import httplib2
except ImportError:
    print('httplib2 not found on this machine. You can download it here. https://github.com/fffonion/httplib2-plus')
#key_cntw={'res': '*'*16,'helper':'*'*16,'crypt':'*'*16
#    }
key_cntw={'res': '*'*16,'helper':'*'*16,'crypt':'*'*16
    }
key_jp={'res': 'A1dPUcrvur2CRQyl','helper':'A1dPUcrvur2CRQyl','crypt':'uH9JF2cHf6OppaC1'
    }

serv={'cn':'http://game1-CBT.ma.sdo.com:10001/connect/app/','cn_data':'http://MA.webpatch.sdg-china.com/',
    'cn2':'http://game2-CBT.ma.sdo.com:10001/connect/app/','cn2_data':'http://MA.webpatch.sdg-china.com/',
    'tw':'http://game.ma.mobimon.com.tw:10001/connect/app/','tw_data':'http://download.ma.mobimon.com.tw/',
    'jp':'http://web.million-arthurs.com/connect/app/','jp_data':''
    }

headers_main={'User-Agent': 'Million/100 (GT-I9100; GT-I9100; 2.3.4) samsung/GT-I9100/GT-I9100:2.3.4/GRJ22/eng.build.20120314.185218:eng/release-keys','Connection': 'Keep-Alive','Accept-Encoding':'gzip,deflate'}
headers_post={'Content-Type': 'application/x-www-form-urlencoded'}

SLOW_MODE=False
def init_cipher(loc='cn'):
    if loc in ['cn','tw']:
        _key=key_cntw
    else:
        _key=key_jp
    try:
        from Crypto.Cipher import AES
        return AES.new(_key['res'], AES.MODE_ECB),\
            AES.new(_key['crypt'], AES.MODE_ECB),\
            False
    except ImportError:
        import pyaes
        return pyaes.new(_key['res'], pyaes.MODE_ECB),\
            pyaes.new(_key['crypt'], pyaes.MODE_ECB),\
            True
COD_RES,COD_DATA,SLOW_MODE=init_cipher()

BS=16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1])]
du8=lambda str:str.decode('utf-8')
ht=httplib2.Http(timeout=15)
def decode_res(bytein):
    return COD_RES.decrypt(bytein)

def decode_data(bytein):
    if len(bytein)==0:
        return ''
    else:
        return unpad(COD_DATA.decrypt(bytein))

def decode_data64(strin):
    return decode_data(base64.decodestring(urlescape(strin)))

def encode_data(bytein):
    return COD_DATA.encrypt(pad(bytein))

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
    def __init__(self,loc,logger,ua):
        self.cookie=''
        #self.maClientInstance=mac
        self.servloc=loc
        self.logger=logger
        self.header=headers_main
        self.header.update(headers_post)
        if loc in ['jp','kr']:
            COD_RES,COD_DATA=init_cipher(loc=loc)[:2]
            ua='Million/235 (GT-I9100; GT-I9100; 2.3.4) samsung/GT-I9100/GT-I9100:2.3.4/GRJ22/eng.build.20120314.185218:eng/release-keys GooglePlay'
        if ua:
            self.header['User-Agent']=ua
        if SLOW_MODE:
            self.logger.warning(du8('post:没有安装pycrypto库，可能将额外耗费大量时间'))
        self.issavetraffic=False

    def set_cookie(self,cookie):
        self.cookie=cookie

    def enable_savetraffic(self):
        self.issavetraffic=True

    def update_server(self,check_inspection_str):
        if check_inspection_str:
            strs=check_inspection_str.split(',')
            try:
                serv[self.servloc]=strs[3]
                serv['%s_data'%self.servloc]=strs[2]
            except KeyError:
                pass
            except IndexError:
                self.logger.error(du8('错误的密钥？'))
                raw_input()
                os._exit(1)

    def post(self,uri,postdata='',usecookie=True,setcookie=True,extraheader={'Cookie2': '$Version=1'},noencrypt=False,savetraffic=False):
            header={}
            header.update(self.header)
            header.update(extraheader)
            if usecookie:
                header.update({'Cookie':self.cookie})
            if not noencrypt and postdata!='':
                postdata=encode_param(postdata)
            trytime=0
            ttimes=3
            callback_hook=None
            if savetraffic and self.issavetraffic:
                callback_hook=lambda x:x
            while trytime<ttimes:
                try:
                    resp,content=ht.request('%s%s%s'%(serv[self.servloc],uri,not noencrypt and '?cyt=1' or ''),method='POST',headers=header,body=postdata,callback_hook=callback_hook,chunk_size=None)
                except socket.error as e:
                    if e.errno==None:
                        err='Timed out'
                    else:
                        err=e.errno
                    self.logger.warning('post:%s got socket error:%s, retrying in %d times'%(uri,err,ttimes-trytime))
                except httplib.ResponseNotReady:
                    #socket重置，不计入重试次数
                    trytime-=1
                    self.logger.warning('post:socket closed, retrying in %d times'%(ttimes-trytime))
                except httplib2.ServerNotFoundError:
                    self.logger.warning('post:no internet, retrying in %d times'%(ttimes-trytime))
                else:
                    if int(resp['status'])<400:
                        break
                    self.logger.warning('post:POSTing %s, server returns code %s, retrying in %d times'%(uri,resp['status'],3-trytime))
                resp,content={'status':'0'},''
                trytime+=1
                time.sleep(2.718281828*trytime)
            if not 'content-length' in resp:
                resp['content-length']=str(len(content))
            #状态码判断
            if int(resp['status'])>400:
                self.logger.error('post:%s %s'%(uri,','.join([ ( i in resp and (i+':'+resp[i]) or '' )for i in ['status','content-length','set-cookie']])+du8('\n请到信号良好的地方重试【←←')))
                resp.update({'error':True,'errno':resp['status'],'errmsg':'Client or server error.'})
                return resp,content
            else:
                self.logger.debug('post:%s %s'%(uri,','.join([ ( i in resp and (i+':'+resp[i]) or '' )for i in ['status','content-length','set-cookie']])))
            #省流模式
            if savetraffic and self.issavetraffic:
                return resp,content
            #否则解码
            dec=decode_data(content)
            if os.path.exists('debug'):
                open('debug/%s.xml'%uri.replace('/','#').replace('?','~'),'w').write(dec)
                open('debug/~%s.xml'%uri.replace('/','#').replace('?','~'),'w').write(content)
            if setcookie and 'set-cookie' in resp:
                self.cookie=resp['set-cookie'].split(',')[-1].rstrip('path=/').strip()
            #print self.cookie
            return resp,dec

if __name__=="__main__":
    print(decode_param('S=l%2BSLkFbck3jK7ftUq4XEWUgdXcgDbKVDRxUYqRmWhpE%3D%0A&revision=NzgOGTK08BvkZN5q8XvG6Q%3D%3D%0A'))