#!/usr/bin/env python
# coding:utf-8
# maclient network utility
# Contributor:
#      fffonion        <fffonion@gmail.com>
import os
import re
import sys
import time
import base64
import socket
import urllib
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
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_v1_5
    SLOW_MODE = False
except ImportError:
    import pyaes as AES
    SLOW_MODE=True


serv = {'cn':'http://game1-CBT.ma.sdo.com:10001/connect/app/',
    'cn2':'http://game2-CBT.ma.sdo.com:10001/connect/app/', 
    'cn3':'http://game3-CBT.ma.sdo.com:10001/connect/app/',
    'tw':'http://game.ma.mobimon.com.tw:10001/connect/app/',
    'jp':'http://web.million-arthurs.com/connect/app/', 'jp_data':'',
    'kr':'http://ma.actoz.com:10001/connect/app/', 'kr_data':''}
serv['cn_data'] = serv['cn2_data'] = serv['cn3_data'] = 'http://MA.webpatch.sdg-china.com/'

headers_main = {'User-Agent': 'Million/%d (GT-I9100; GT-I9100; 2.3.4) samsung/GT-I9100/GT-I9100:2.3.4/GRJ22/eng.build.20120314.185218:eng/release-keys', 'Connection': 'Keep-Alive', 'Accept-Encoding':'gzip,deflate'}
headers_post = {'Content-Type': 'application/x-www-form-urlencoded'}

pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
unpad = lambda s : s[0:-ord(s[-1])]
b2u = PYTHON3 and (lambda x:x.decode(encoding = 'utf-8')) or (lambda x:x)
MOD_AES, MOD_AES_RANDOM, MOD_RSA_AES_RANDOM = 0, 1, 2
class Crypt():
    def __init__(self,loc):
        self.init_cipher(loc=loc)
        self.random_cipher_plain=''
        if loc in ['cn','tw']:
            self.gen_rsa_pubkey()
        self.AES2ndKey = None

    def gen_cipher_with_uid(self, uid, loc):
        plain = '%s%s%s' % (getattr(maclient_smart, 'key_%s' % loc[:2])['crypt'][:16], uid, '0'*(16-len(uid)))
        return self._gen_cipher(plain)

    def gen_rsa_pubkey(self):
        #pk="""MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAM5U06JAbYWdRBrnMdE2bEuDmWgUav7xNKm7i8s1Uy/\nfvpvfxLeoWowLGIBKz0kDLIvhuLV8Lv4XV0+aXdl2j4kCAwEAAQ=="""
        pk = maclient_smart.key_rsa_pool[2]
        #pk = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A' + ''.join(pk[1:-2])
        pk = [pk[i:i+64] for i in range(0, len(pk), 64)]
        pk = '-----BEGIN PUBLIC KEY-----\n' + '\n'.join(pk) + '\n-----END PUBLIC KEY-----'
        #print pk
        self.rsa = PKCS1_v1_5.new(RSA.importKey(pk))
        #bio = BIO.MemoryBuffer(pk) # pk is ASCII, don't encode
        #self.rsa = RSA.load_pub_key_bio(bio)

    def gen_random_cipher(self):
        self.random_cipher_plain=os.urandom(16)
        self.random_cipher = self._gen_cipher(self.random_cipher_plain)

    def _gen_cipher(self,plain):
        return AES.new(plain, AES.MODE_ECB)

    def init_cipher(self,loc = 'cn', uid = None):
        _key = getattr(maclient_smart, 'key_%s' % loc[:2])
        if loc == 'jp':
            #if not uid:
            #    uid = '0'
            _key['crypt'] = '%s%s' % (_key['crypt'], '0' * 16)
        if sys.platform == 'cli':
            pass  # import clr
            # clr.AddReference("IronPyCrypto.dll")
        self.cipher_data = self._gen_cipher(_key['crypt'])
        self.cipher_res = self._gen_cipher(_key['res'])

    def decode_res(self, bytein):
        return self.cipher_res.decrypt(bytein)

    def decode_data(self, bytein, second_cipher = False):
        if len(bytein) == 0:
            return ''
        else:
            if second_cipher:
                return unpad(b2u(self.AES2ndKey.decrypt(bytein)))
            else:
                return unpad(b2u(self.cipher_data.decrypt(bytein)))

    def decode_data64(self, strin):
        return self.decode_data(base64.decodestring(self.urlescape(strin)))

    def encode_data(self, bytein, mode):
        if mode==MOD_AES:
            return self.cipher_data.encrypt(pad(bytein))
        elif mode >= MOD_AES_RANDOM:
            return self.random_cipher.encrypt(pad(bytein))

    def encode_rsa_64(self, strin):
        return base64.encodestring(self.rsa.encrypt(strin))

    def encode_data64(self, bytein, mode):
        res=b2u(base64.encodestring(self.encode_data(bytein, mode))).strip('\n')
        # if mode != MOD_RSA_AES_RANDOM:
        #     return self.urlunescape(res)
        return res

    def encode_param(self, param, mode = MOD_AES, second_cipher = False):
        p = param.split('&')
        if mode == MOD_RSA_AES_RANDOM:
            _m=self.encode_rsa_64
        else:
            _m=lambda x:x
        if second_cipher: #replace
            self.AES2ndKey, self.cipher_data = self.cipher_data, self.AES2ndKey
        p_enc = '%0A&'.join(['%s=%s' % (p[i].split('=')[0], self.urlunescape(_m(self.encode_data64(p[i].split('=')[1], mode)))) for i in xrange(len(p))])
        if second_cipher: #rollback
            self.AES2ndKey, self.cipher_data = self.cipher_data, self.AES2ndKey
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

#ht = httplib2.Http(timeout = 15,proxy_info = httplib2.ProxyInfo(httplib2.socks.PROXY_TYPE_HTTP_NO_TUNNEL, "192.168.124.1", 23300))
def htmlescape(htmlstr):
    def replc(match):
        # self._print match.group(0),match.group(1),match.group(2)
        dict = {'amp':'&', 'nbsp':' ', 'quot':'"', 'lt':'<', 'gt':'>', 'copy':'©', 'reg':'®'}
        # dict+={'∀':'forall','∂':'part','∃':'exist','∅':'empty','∇':'nabla','∈':'isin','∉':'notin','∋':'ni','∏':'prod','∑':'sum','−':'minus','∗':'lowast','√':'radic','∝':'prop','∞':'infin','∠':'ang','∧':'and','∨':'or','∩':'cap','∪':'cup','∫':'int','∴':'there4','∼':'sim','≅':'cong','≈':'asymp','≠':'ne','≡':'equiv','≤':'le','≥':'ge','⊂':'sub','⊃':'sup','⊄':'nsub','⊆':'sube','⊇':'supe','⊕':'oplus','⊗':'otimes','⊥':'perp','⋅':'sdot','Α':'Alpha','Β':'Beta','Γ':'Gamma','Δ':'Delta','Ε':'Epsilon','Ζ':'Zeta','Η':'Eta','Θ':'Theta','Ι':'Iota','Κ':'Kappa','Λ':'Lambda','Μ':'Mu','Ν':'Nu','Ξ':'Xi','Ο':'Omicron','Π':'Pi','Ρ':'Rho','Σ':'Sigma','Τ':'Tau','Υ':'Upsilon','Φ':'Phi','Χ':'Chi','Ψ':'Psi','Ω':'Omega','α':'alpha','β':'beta','γ':'gamma','δ':'delta','ε':'epsilon','ζ':'zeta','η':'eta','θ':'theta','ι':'iota','κ':'kappa','λ':'lambda','μ':'mu','ν':'nu','ξ':'xi','ο':'omicron','π':'pi','ρ':'rho','ς':'sigmaf','σ':'sigma','τ':'tau','υ':'upsilon','φ':'phi','χ':'chi','ψ':'psi','ω':'omega','ϑ':'thetasym','ϒ':'upsih','ϖ':'piv','Œ':'OElig','œ':'oelig','Š':'Scaron','š':'scaron','Ÿ':'Yuml','ƒ':'fnof','ˆ':'circ','˜':'tilde',' ':'ensp',' ':'emsp',' ':'thinsp','‌':'zwnj','‍':'zwj','‎':'lrm','‏':'rlm','–':'ndash','—':'mdash','‘':'lsquo','’':'rsquo','‚':'sbquo','“':'ldquo','”':'rdquo','„':'bdquo','†':'dagger','‡':'Dagger','•':'bull','…':'hellip','‰':'permil','′':'prime','″':'Prime','‹':'lsaquo','›':'rsaquo','‾':'oline','€':'euro','™':'trade','←':'larr','↑':'uarr','→':'rarr','↓':'darr','↔':'harr','↵':'crarr','⌈':'lceil','⌉':'rceil','⌊':'lfloor','⌋':'rfloor','◊':'loz','♠':'spades','♣':'clubs','♥':'hearts','♦':'diams'}
        if match.groups > 2:
            if match.group(1) == '#':
                if match.group(2).startswith('x'):#xD, xA
                    return unichr(int(match.group(2)[1:],16))
                else:
                    return unichr(int(match.group(2)))
            else:
                return  dict.get(match.group(2), '?')
    htmlre = re.compile("&(#?)(\d{1,5}|\w{1,8}|[a-z]+);")
    return htmlre.sub(replc, htmlstr)

class poster():
    def __init__(self, loc, logger, ua):
        self.cookie = ''
        self.ht = httplib2.Http(timeout = 15)
        # ironpython版的httplib2的iri2uri中用utf-8代替了idna，因此手动变回来
        self.rollback_utf8 = sys.platform.startswith('cli') and \
                (lambda dt:dt.decode('utf-8')) or\
                (lambda dt:dt)
        self.logger = logger
        self.load_svr(loc, ua)
        if SLOW_MODE:
            self.logger.warning(du8('post:没有安装pycrypto库，可能将额外耗费大量时间'))
        self.issavetraffic = False
        

    def set_cookie(self, cookie):
        self.cookie = cookie

    def enable_savetraffic(self):
        self.issavetraffic = True

    def gen_2nd_key(self, uid, loc='jp'):
        self.crypt.AES2ndKey = self.crypt.gen_cipher_with_uid(uid, loc)

    def load_svr(self, loc, ua=''):
        self.servloc = loc
        self.shortloc = loc[:2]
        self.header = dict(headers_main)
        self.header.update(headers_post)
        if ua != '':
            if '%d' in ua:  # formatted ua
                self.header['User-Agent'] = ua % getattr(maclient_smart, 'app_ver_%s' % self.shortloc)
            else:
                self.header['User-Agent'] = ua
        else:
            self.header['User-Agent'] = self.header['User-Agent'] % getattr(maclient_smart, 'app_ver_%s' % self.shortloc)
        if self.shortloc in ['cn','kr']:
            self.ht.add_credentials("iW7B5MWJ", "8KdtjVfX")
        elif self.servloc == 'jp':
            self.ht.add_credentials("eWa25vrE", "2DbcAh3G")
            if (not self.header['User-Agent'].endswith('GooglePlay')):
                self.header['User-Agent'] += 'GooglePlay'
        self.has_2ndkey = loc =='jp'
        self.crypt=Crypt(self.shortloc)

    def update_server(self, check_inspection_str):
        #not using
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

    def post(self, uri, postdata = '', usecookie = True, setcookie = True, extraheader = {'Cookie2': '$Version=1'}, noencrypt = False, savetraffic = False, no2ndkey = False):#no2ndkey only used in jp server
            header = {}
            header.update(self.header)
            header.update(extraheader)
            if usecookie:
                header.update({'Cookie':self.cookie})
            if not noencrypt :
                if self.shortloc in ['cn','tw']:#pass key to server
                    #add sign to param
                    self.crypt.gen_random_cipher()
                    sign='K=%s'%self.crypt.urlunescape(
                        self.crypt.encode_rsa_64(
                            base64.encodestring(
                                self.crypt.random_cipher_plain))).rstrip('\n')
                    if postdata:#has real stuff
                        if uri in ['login','regist']:
                            postdata = self.crypt.encode_param(postdata.encode('utf-8'), mode=MOD_RSA_AES_RANDOM)
                        else:
                            postdata = self.crypt.encode_param(postdata, mode=MOD_AES_RANDOM)
                        postdata='&'.join([sign,postdata])
                    else:
                        postdata=sign
                elif postdata != '':
                    postdata = self.crypt.encode_param(postdata, second_cipher = self.has_2ndkey and not no2ndkey)  
            trytime = 0
            ttimes = 3
            callback_hook = None
            if savetraffic and self.issavetraffic:
                callback_hook = lambda x:x
            while trytime < ttimes:
                try:
                    resp, content = self.ht.request('%s%s%s' % (serv[self.servloc], uri, not noencrypt and '?cyt=1' or ''), method = 'POST', headers = header, body = postdata, callback_hook = callback_hook, chunk_size = None)
                except socket.error as e:
                    if e.errno == None:
                        err = 'Timed out'
                    else:
                        err = e.errno
                    self.logger.warning('post:%s got socket error:%s, retrying in %d times' % (uri, err, ttimes - trytime))
                except httplib.BadStatusLine:
                    self.logger.warning('post:%s malformed response retrying in %d times' % (uri, ttimes - trytime))
                except httplib.ResponseNotReady:
                    # socket重置，不计入重试次数
                    trytime -= 1
                    self.logger.warning('post:socket closed, retrying in %d times' % (ttimes - trytime))
                except httplib2.ServerNotFoundError:
                    self.logger.warning('post:no internet, retrying in %d times' % (ttimes - trytime))
                except TypeError:  # 使用了官方版的httplib2
                    if savetraffic and self.issavetraffic:
                        self.logger.warning(du8('你正在使用官方版的httplib2，因此省流模式将无法正常工作'))
                    resp, content = self.ht.request('%s%s%s' % (serv[self.servloc], uri, not noencrypt and '?cyt=1' or ''), method = 'POST', headers = header, body = postdata)
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
            dec = self.rollback_utf8(self.crypt.decode_data(content, second_cipher = self.has_2ndkey and not no2ndkey))
            if os.path.exists('debug'):
                open('debug/%s.xml' % uri.replace('/', '#').replace('?', '~'), 'w').write(dec)
                # open('debug/~%s.xml'%uri.replace('/','#').replace('?','~'),'w').write(content)
            if setcookie and 'set-cookie' in resp:
                self.cookie = resp['set-cookie'].split(',')[-1].rstrip('path=/').strip()
            # print self.cookie
            return resp, dec

if __name__ == "__main__":
    p = Crypt('cn')
    p.gen_random_cipher() 
