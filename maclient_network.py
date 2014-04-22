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
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5


serv = {'cn':'http://game1-CBT.ma.sdo.com:10001/connect/app/',
    'cn2':'http://game2-CBT.ma.sdo.com:10001/connect/app/', 
    'cn3':'http://game3-CBT.ma.sdo.com:10001/connect/app/',
    'tw':'http://game.ma.mobimon.com.tw:10001/connect/app/','tw_data':'http://download.ma.mobimon.com.tw/',
    'jp':'http://web.million-arthurs.com/connect/app/', 'jp_data':'',
    'kr':'http://ma.actoz.com:10001/connect/app/', 'kr_data':'',
    'sg':'http://playma.cherrycredits.com:10001/connect/app/', 'sg_data':''}
serv['cn1'] = serv['cn']
serv['cn_data'] = serv['cn2_data'] = serv['cn3_data'] = 'http://MA.webpatch.sdg-china.com/'

headers_main = {'User-Agent': 'Million/%d (GT-I9100; GT-I9100; 2.3.4) samsung/GT-I9100/GT-I9100:2.3.4/GRJ22/eng.build.20120314.185218:eng/release-keys', 'Connection': 'Keep-Alive'}#, 'Accept-Encoding':'gzip,deflate'}
headers_post = {'Content-Type': 'application/x-www-form-urlencoded'}

pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
unpad = lambda s : s[0:-ord(s[-1])]
b2u = PYTHON3 and (lambda x:x.decode(encoding = 'utf-8', errors = 'replace')) or (lambda x:x)
tobytes = PYTHON3 and (lambda x:x if isinstance(x, bytes) else x.encode(encoding = 'utf-8', errors = 'replace')) or (lambda x:x)
MOD_AES, MOD_AES_RANDOM, MOD_RSA_AES_RANDOM = 0, 1, 2
class Crypt():
    def __init__(self,loc):
        self.init_cipher(loc=loc)
        self.random_cipher_plain=''
        if not loc == 'jp':
            self.gen_rsa_pubkey()
            # if loc in ['kr', 'sg']:
            #     import string
            #     import random
            #     self._gen_rnd_key = lambda x = 16 : ''.join([random.choice(string.letters + string.digits) for i in range(x)])
            # else:
            #     self._gen_rnd_key = lambda x = 16 : os.urandom(x)
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
        self.random_cipher_plain = os.urandom(16)
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
        return b2u(base64.encodestring(self.rsa.encrypt(tobytes(strin))))

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
        p_enc = '%0A&'.join(['%s=%s' % (p[i].split('=')[0], self.urlunescape(_m(self.encode_data64(p[i].split('=')[1], mode)))) for i in range(len(p))])
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
        dict = {'amp':'&', 'nbsp':' ', 'quot':'"', 'lt':'<', 'gt':'>', 'copy':'漏', 'reg':'庐'}
        # dict+={'鈭€':'forall','鈭:'part','鈭:'exist','鈭:'empty','鈭:'nabla','鈭:'isin','鈭:'notin','鈭:'ni','鈭:'prod','鈭:'sum','鈭:'minus','鈭:'lowast','鈭:'radic','鈭:'prop','鈭:'infin','鈭:'ang','鈭:'and','鈭:'or','鈭:'cap','鈭:'cup','鈭:'int','鈭:'there4','鈭:'sim','鈮:'cong','鈮:'asymp','鈮:'ne','鈮:'equiv','鈮:'le','鈮:'ge','鈯:'sub','鈯:'sup','鈯:'nsub','鈯:'sube','鈯:'supe','鈯:'oplus','鈯:'otimes','鈯:'perp','鈰:'sdot','螒':'Alpha','螔':'Beta','螕':'Gamma','螖':'Delta','螘':'Epsilon','螙':'Zeta','螚':'Eta','螛':'Theta','螜':'Iota','螝':'Kappa','螞':'Lambda','螠':'Mu','螡':'Nu','螢':'Xi','螣':'Omicron','螤':'Pi','巍':'Rho','危':'Sigma','韦':'Tau','违':'Upsilon','桅':'Phi','围':'Chi','唯':'Psi','惟':'Omega','伪':'alpha','尾':'beta','纬':'gamma','未':'delta','蔚':'epsilon','味':'zeta','畏':'eta','胃':'theta','喂':'iota','魏':'kappa','位':'lambda','渭':'mu','谓':'nu','尉':'xi','慰':'omicron','蟺':'pi','蟻':'rho','蟼':'sigmaf','蟽':'sigma','蟿':'tau','蠀':'upsilon','蠁':'phi','蠂':'chi','蠄':'psi','蠅':'omega','蠎':'thetasym','蠏':'upsih','蠔':'piv','艗':'OElig','艙':'oelig','艩':'Scaron','拧':'scaron','鸥':'Yuml','茠':'fnof','藛':'circ','藴':'tilde','鈥:'ensp','鈥:'emsp','鈥:'thinsp','鈥:'zwnj','鈥:'zwj','鈥:'lrm','鈥:'rlm','鈥:'ndash','鈥:'mdash','鈥:'lsquo','鈥:'rsquo','鈥:'sbquo','鈥:'ldquo','鈥:'rdquo','鈥:'bdquo','鈥:'dagger','鈥:'Dagger','鈥:'bull','鈥:'hellip','鈥:'permil','鈥:'prime','鈥:'Prime','鈥:'lsaquo','鈥:'rsaquo','鈥:'oline','鈧:'euro','鈩:'trade','鈫:'larr','鈫:'uarr','鈫:'rarr','鈫:'darr','鈫:'harr','鈫:'crarr','鈱:'lceil','鈱:'rceil','鈱:'lfloor','鈱:'rfloor','鈼:'loz','鈾:'spades','鈾:'clubs','鈾:'hearts','鈾:'diams'}
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
        self.ht = httplib2.Http(timeout = 20)
        # ironpython版的httplib2的iri2uri中用utf-8代替了idna，因此手动变回来
        self.rollback_utf8 = sys.platform.startswith('cli') and \
                (lambda dt:dt.decode('utf-8')) or\
                (lambda dt:dt)
        self.logger = logger
        self.load_svr(loc, ua)
        self.issavetraffic = False
        

    def set_cookie(self, cookie):
        if not cookie.endswith(';'):
            cookie += ';'
        self.cookie = cookie

    def enable_savetraffic(self):
        if httplib2.__version__.endswith('+'):
            self.issavetraffic = True
        else:
            self.logger.warning('你正在使用官方版的httplib2，因此省流模式将无法正常工作')

    def gen_2nd_key(self, uid, loc='jp'):
        self.crypt.AES2ndKey = self.crypt.gen_cipher_with_uid(uid, loc)

    def load_svr(self, loc, ua=''):
        self.ht = httplib2.Http(timeout = 15)
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
        if self.shortloc in ['cn','kr','sg']:
            self.ht.add_credentials("iW7B5MWJ", "8KdtjVfX")
        elif self.servloc == 'jp':
            self.ht.add_credentials("eWa25vrE", "2DbcAh3G")
            if (not self.header['User-Agent'].endswith('GooglePlay')):
                self.header['User-Agent'] += 'GooglePlay'
            self.v = '.'.join(list(str(maclient_smart.app_ver_jp)))#like 304 -> 3.0.4
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
                
    def set_timeout(self, timeout):
        self.ht.timeout = timeout

    def post(self, uri, postdata = '', usecookie = True, setcookie = True, extraheader = {'Cookie2': '$Version=1'}, noencrypt = False, savetraffic = False, no2ndkey = False):#no2ndkey only used in jp server
            header = {}
            header.update(self.header)
            header.update(extraheader)
            if usecookie and not self.has_2ndkey:
                header.update({'Cookie':self.cookie})
            if not noencrypt :
                if not self.shortloc == 'jp':#pass key to server
                    #add sign to param
                    self.crypt.gen_random_cipher()
                    sign='K=%s'%self.crypt.urlunescape(
                        self.crypt.encode_rsa_64(
                            base64.encodestring(
                                self.crypt.random_cipher_plain))).rstrip('\n')
                    if postdata:#has real stuff
                        if uri in ['login','regist'] and self.shortloc not in ['kr', 'sg']:
                            postdata = self.crypt.encode_param(postdata, mode=MOD_RSA_AES_RANDOM) #remove .encode('utf-8')
                        else:
                            postdata = self.crypt.encode_param(postdata, mode=MOD_AES_RANDOM)
                        postdata='&'.join([sign,postdata])
                    else:
                        postdata=sign
                else:#for jp
                    #S=cookie&cyt=1&v=encrypted(x.x.x)&encoded_param
                    if postdata:
                        postdata += '&'
                    postdata =  '%s%s&%s' % (
                        self.cookie[:-1], not noencrypt and '&cyt=1' or '',
                        self.crypt.encode_param('%sv=%s'% (postdata, self.v), second_cipher = self.has_2ndkey and not no2ndkey)
                        )
                    extraheader = {}
            trytime = 0
            ttimes = 3
            extra_kwargs = {}
            if savetraffic and self.issavetraffic:
                extra_kwargs = {'callback_hook' : lambda x:x, 'chunk_size' : None}
            while trytime < ttimes:
                try:
                    resp, content = self.ht.request('%s%s%s' % (serv[self.servloc], uri, \
                        (not noencrypt and not self.has_2ndkey) and '?cyt=1' or ''), \
                        method = 'POST', headers = header, body = postdata, **extra_kwargs)
                    assert(len(content) > 0 or (savetraffic and self.issavetraffic) or resp['status'] == '302')
                except socket.error as e:
                    if e.errno == None:
                        err = 'Timed out'
                    else:
                        err = e.errno
                    self.logger.warning('post:%s got socket error:%s, retrying in %d times' % (uri, err, ttimes - trytime))
                except AssertionError:
                    self.logger.warning('post:%s got empty response , retrying in %d times' % (uri, ttimes - trytime))
                except httplib.BadStatusLine:
                    self.logger.warning('post:%s malformed response, retrying in %d times' % (uri, ttimes - trytime))
                except httplib.ResponseNotReady:
                    # socket重置，不计入重试次数
                    trytime -= ( 1 if trytime > 1 else 0 )
                    self.logger.warning('post:socket closed, retrying in %d times' % (ttimes - trytime))
                except httplib2.ServerNotFoundError:
                    self.logger.warning('post:no internet, retrying in %d times' % (ttimes - trytime))
                # except TypeError:  # 使用了官方版的httplib2
                #     self.logger.warning(du8('你正在使用官方版的httplib2，因此省流模式将无法正常工作'))
                #     self.issavetraffic = False
                #     extra_kwargs = {}
                #     trytime += 1 #不算
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
