#!/usr/bin/env python
# coding:utf-8
# maclient network utility
# Contributor:
#      fffonion        <fffonion@gmail.com>
import os
import sys
import time
import base64
import socket
import urllib
from M2Crypto import BIO, RSA
import maclient_smart
from cross_platform import *
if PYTHON3:
    import http.client as httplib
    xrange = range
else:
    import httplib
try:
    import httplib2
except ImportError:
    print('httplib2 not found in python libs. You can download it here: https://github.com/fffonion/httplib2-plus')
try:
    from Crypto.Cipher import AES
    SLOW_MODE = False
except ImportError:
    import pyaes as AES
    SLOW_MODE=True


serv = {'cn':'http://game1-CBT.ma.sdo.com:10001/connect/app/', 'cn_data':'http://MA.webpatch.sdg-china.com/',
    'cn2':'http://game2-CBT.ma.sdo.com:10001/connect/app/', 'cn2_data':'http://MA.webpatch.sdg-china.com/',
    'cn3':'http://game3-CBT.ma.sdo.com:10001/connect/app/', 'cn2_data':'http://MA.webpatch.sdg-china.com/',
    'tw':'http://game.ma.mobimon.com.tw:10001/connect/app/', 'tw_data':'http://download.ma.mobimon.com.tw/',
    'jp':'http://web.million-arthurs.com/connect/app/', 'jp_data':'',
    'kr':'http://ma.actoz.com:10001/connect/app/', 'kr_data':''
    }

headers_main = {'User-Agent': 'Million/%d (GT-I9100; GT-I9100; 2.3.4) samsung/GT-I9100/GT-I9100:2.3.4/GRJ22/eng.build.20120314.185218:eng/release-keys', 'Connection': 'Keep-Alive', 'Accept-Encoding':'gzip,deflate'}
headers_post = {'Content-Type': 'application/x-www-form-urlencoded'}

pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
unpad = lambda s : s[0:-ord(s[-1])]
b2u = PYTHON3 and (lambda x:x.decode(encoding = 'utf-8')) or (lambda x:x)
MOD_AES, MOD_AES_RANDOM, MOD_RSA = 1, 2, 0
class Crypt():
    def __init__(self,loc):
        self.init_cipher(loc=loc)
        self.random_cipher_plain=''
        if loc=='cn':
            gen_rsa_pubkey()

    def gen_cipher_with_uid(self,uid):
        pass

    def gen_rsa_pubkey(self):
        pk="""MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAM5U06JAbYWdRBrnMdE2bEuDmWgUav7xNKm7i8s1Uy/\nfvpvfxLeoWowLGIBKz0kDLIvhuLV8Lv4XV0+aXdl2j4kCAwEAAQ=="""
        #pk = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A' + ''.join(pk[1:-2])
        pk = [pk[i:i+64] for i in range(0, len(pk), 64)]
        pk = '-----BEGIN PUBLIC KEY-----\n' + '\n'.join(pk) + '\n-----END PUBLIC KEY-----'
        #print pk
        bio = BIO.MemoryBuffer(pk) # pk is ASCII, don't encode
        self.rsa = RSA.load_pub_key_bio(bio)

    def gen_random_cipher(self):
        self.random_cipher_plain=os.urandom(16)
        return self.random_cipher(self.random_cipher_plain)

    def _gen_cipher(self,plain):
        return AES.new(plain, AES.MODE_ECB)

    def init_cipher(self,loc = 'cn', uid = None):
        _key = getattr(maclient_smart, 'key_%s' % loc)
        if loc == 'jp':
            if not uid:
                uid = '0'
            _key['crypt'] = '%s%s%s' % (_key['crypt'], uid, '0' * (32 - len(_key['crypt'] + uid)))
            print(_key['crypt'])
        if sys.platform == 'cli':
            pass  # import clr
            # clr.AddReference("IronPyCrypto.dll")
        self.cipher_data = self._gen_cipher(_key['crypt'])
        self.cipher_res = self._gen_cipher(_key['res'])

    def decode_res(self, bytein):
        return cipher.decrypt(bytein)

    def decode_data(self, bytein):
        if len(bytein) == 0:
            return ''
        else:
            return unpad(b2u(self.cipher_data.decrypt(bytein)))

    def decode_data64(self, strin):
        return self.decode_data(base64.decodestring(self.urlescape(strin)))

    def encode_data(self, bytein, mode):
        if mode==MOD_AES:
            return self.cipher_data.encrypt(pad(bytein))
        elif mode==MOD_AES_RANDOM:
            return self.random_cipher.encrypt(pad(bytein))
        elif mode==MOD_RSA:
            rst=self.rsa.public_encrypt(message, RSA.pkcs1_padding)
            return base64.encodestring(rst)

    def encode_data64(self, bytein, mode):
        return self.urlunescape(b2u(base64.encodestring(self.encode_data(bytein, mode))).strip('\n'))

    def encode_param(self, param, mode=MOD_AES):
        p = param.split('&')
        p_enc = '%0A&'.join(['%s=%s' % (p[i].split('=')[0], self.encode_data64(p[i].split('=')[1], mode)) for i in xrange(len(p))])
        # print p_enc
        return p_enc.replace('\n', '')

    def decode_param(self, param_enc):
        p_enc = param_enc.split('&')
        p = '%0A&'.join(['%s=%s' % (p_enc[i].split('=')[0], self.decode_data64(p_enc[i].split('=')[1])) for i in xrange(len(p_enc))])
        return p

    #modified '&' to '\n'
    def urlunescape(self, url):
        return url.replace('=', '%3D').replace('\n', '%0A').replace('/', '%2F').replace('+', '%2B')

    def urlescape(self, url):
        return url.replace('%3D', '=').replace('%0A', '\n').replace('%2F', '/').replace('%2B', '+')

    def decrypt_file(self, filein, fileout, ext = 'png'):
        fileout = '%s.%s' % (fileout, ext)
        if not os.path.exists(os.path.split(fileout)[0]):
            os.makedirs(os.path.split(fileout)[0])
        try:
            if not os.path.exists(fileout):
                open(fileout, 'wb').write(decode_res(open(filein, 'rb').read()))
        except ValueError:
            print('skip', filein)
        else:
            pass

ht = httplib2.Http(timeout = 15)



class poster():
    def __init__(self, loc, logger, ua):
        self.cookie = ''
        # self.maClientInstance=mac
        self.servloc = loc[:2]
        self.logger = logger
        self.header = headers_main
        self.header.update(headers_post)
        # ironpython版的httplib2的iri2uri中用utf-8代替了idna，因此手动变回来
        self.rollback_utf8 = sys.platform.startswith('cli') and \
                (lambda dt:dt.decode('utf-8')) or\
                (lambda dt:dt)
        if self.servloc in ['cn','kr']:
            ht.add_credentials("iW7B5MWJ", "8KdtjVfX")
        if ua:
            if '%d' in ua:  # formatted ua
                self.header['User-Agent'] = ua % getattr(maclient_smart, 'app_ver_%s' % self.servloc)
            else:
                self.header['User-Agent'] = ua
        else:
            self.header['User-Agent'] = self.header['User-Agent'] % getattr(maclient_smart, 'app_ver_%s' % self.servloc)
        if SLOW_MODE:
            self.logger.warning(du8('post:没有安装pycrypto库，可能将额外耗费大量时间'))
        self.issavetraffic = False
        self.default_2ndkey = loc in ['jp','cn']
        self.crypt=Crypt(loc)

    def set_cookie(self, cookie):
        self.cookie = cookie

    def gen_2nd_key(self, uid = 0, random_key="", loc = 'cn'):
        pass

    def enable_savetraffic(self):
        self.issavetraffic = True

    def update_server(self, check_inspection_str):
        if check_inspection_str:
            strs = check_inspection_str.split(',')
            try:
                serv[self.servloc] = strs[3]
                serv['%s_data' % self.servloc] = strs[2]
            except KeyError:
                pass
            except IndexError:
                self.logger.error(du8('错误的密钥？'))
                raw_input()
                os._exit(1)

    def post(self, uri, postdata = '', usecookie = True, setcookie = True, extraheader = {'Cookie2': '$Version=1'}, noencrypt = False, savetraffic = False, no2ndkey = False):
            header = {}
            header.update(self.header)
            header.update(extraheader)
            if usecookie:
                header.update({'Cookie':self.cookie})
            if not noencrypt and postdata != '':
                if self.servloc=='cn':#pass key to server
                    self.crypt.gen_random_cipher()
                    postdata='K=%s&%s'%(self.crypt.urlescape(base64.encodestring(self.crypt.random_cipher_plain)),postdata)
                    if uri in ['login','regist']:
                        postdata = encode_param(postdata, mode=MOD_RSA)
                    else:
                        postdata = encode_param(postdata, mode=MOD_AES_RANDOM)
                else:
                    postdata = encode_param(postdata)
            trytime = 0
            ttimes = 3
            callback_hook = None
            if savetraffic and self.issavetraffic:
                callback_hook = lambda x:x
            while trytime < ttimes:
                try:
                    resp, content = ht.request('%s%s%s' % (serv[self.servloc], uri, not noencrypt and '?cyt=1' or ''), method = 'POST', headers = header, body = postdata, callback_hook = callback_hook, chunk_size = None)
                except socket.error as e:
                    if e.errno == None:
                        err = 'Timed out'
                    else:
                        err = e.errno
                    self.logger.warning('post:%s got socket error:%s, retrying in %d times' % (uri, err, ttimes - trytime))
                except httplib.ResponseNotReady:
                    # socket重置，不计入重试次数
                    trytime -= 1
                    self.logger.warning('post:socket closed, retrying in %d times' % (ttimes - trytime))
                except httplib2.ServerNotFoundError:
                    self.logger.warning('post:no internet, retrying in %d times' % (ttimes - trytime))
                except TypeError:  # 使用了官方版的httplib2
                    if savetraffic and self.issavetraffic:
                        self.logger.warning(du8('你正在使用官方版的httplib2，因此省流模式将无法正常工作'))
                    resp, content = ht.request('%s%s%s' % (serv[self.servloc], uri, not noencrypt and '?cyt=1' or ''), method = 'POST', headers = header, body = postdata)
                    break
                else:
                    if int(resp['status']) < 400:
                        break
                    self.logger.warning('post:POSTing %s, server returns code %s, retrying in %d times' % (uri, resp['status'], 3 - trytime))
                resp, content = {'status':'600'}, ''
                trytime += 1
                time.sleep(2.718281828 * trytime)
            if not 'content-length' in resp:
                resp['content-length'] = str(len(content))
            # 状态码判断
            if int(resp['status']) > 400:
                self.logger.error('post:%s %s' % (uri, ','.join([ (i in resp and (i + ':' + resp[i]) or '')for i in ['status', 'content-length', 'set-cookie']]) + du8('\n请到信号良好的地方重试【←←')))
                resp.update({'error':True, 'errno':resp['status'], 'errmsg':'Client or server error.'})
                return resp, content
            else:
                self.logger.debug('post:%s content-length:%s%s' % (uri, resp['content-length'], ('set-cookie' in resp and (' set-cookie:%s' % resp['set-cookie']) or '')))
            # 省流模式
            if savetraffic and self.issavetraffic:
                return resp, content
            # 否则解码
            #open('debug/%s--.xml' % uri.replace('/', '#').replace('?', '~'), 'w').write(content)
            dec = self.rollback_utf8(decode_data(content))
            # open(r'z:/debug/%s.xml'%uri.replace('/','#').replace('?','~'),'w').write(dec)
            if os.path.exists('debug'):
                open('debug/%s.xml' % uri.replace('/', '#').replace('?', '~'), 'w').write(dec)
                # open('debug/~%s.xml'%uri.replace('/','#').replace('?','~'),'w').write(content)
            if setcookie and 'set-cookie' in resp:
                self.cookie = resp['set-cookie'].split(',')[-1].rstrip('path=/').strip()
            # print self.cookie
            return resp, dec

if __name__ == "__main__":
    p = Crypt('cn')
    print([p.encode_param('knight_id=0%0A&move=1%0A&parts_id=0',mode=MOD_AES)])
    # K=eBkWIR2jQTMbtPT%2FVasX0RHVKgNVgeOfpRp4lNBxrX91LlYCoXWVVRj7vgAOXQXrPAsn5aeqmh15%0A5ywC8dL3bA%3D%3D%0A&
    #login_id=TZZjypZKsZ0T4mKpYH%2B1XODqornvgiBW%2B3P3Oe6gZ1WRtlKUMG6%2F5RYNzMJJAsTTV8nYsEW8BHab%0Aj70rlFd%2Fuw%3D%3D%0A&
    #password=SX7az60ooRS3thI64TG2lRUUE%2F6SdJ31tVEI1xZQVKvXeoirwyKYjfBflwkWPrtuOJlT%2BoEgx%2B%2BE%0AoF%2BIuzHHIA%3D%3D%0A
    #K=PiLoUdWGIg%2BpYV5%2FK00XJWAQgjTvvvf2BjGnHxxrq5QTtb5iaXMRQ2hayBebGulyEOcG8%2F2wxMsM%0AJkLk7qaREA%3D%3D%0A&
    #login_id=QkDURvtfZU0WHfBUWd5BtxnXmm85g%2Bz%2F91q2HCwbeAsqJEPymonu7D0I1K5fPqS2ZAjNI7rTWqfT%0AZ3GEmG0KzA%3D%3D%0A&
    #password=GaEVZp6cHKMdDUw3xgSZwskELECVHme7pFWbkO1mwiDNLlDgHT6pWsstydniqWdj0rWPyq2ymbhL%0AA%2F%2FiYvhaUg%3D%3D%0A
#RSA
#MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAM5U06JAbYWdRBrnMdE2bEuDmWgUav7xNKm7i8s1Uy/fvpvfxLeoWowLGIBKz0kDLIvhuLV8Lv4XV0+aXdl2j4kCAwEAAQ==
#AES KEY
#MdWt7g87PkP0uXalsNinqg==
#K=p7QZloUf3nFuyfErUyOW0DwdvYv%2BiDe8KGWUXpE92SPBIIAzu2LTAB0TJyRIAZnnsn0DMmTXnaeS%0AnDWi77bECg%3D%3D%0A
#WO4YqkflLKIWJ3NWCnGpQQ==
#K=EC%2Fys3i5dDM4%2B1oY%2Bkz8Oj38mwoH%2BGSiME%2FrQSFrcIgFrKpxUp%2Fn%2BuH46DRBJgcfPl6nbIZIUT7y%0AkD9LzDLuxw%3D%3D%0A

