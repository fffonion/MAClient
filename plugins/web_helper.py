#coding:utf-8
from _prototype import plugin_prototype
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer  
from SocketServer import ThreadingMixIn
from cStringIO import StringIO
import gzip
import socket
import _webbrowser as webbrowser
import urllib2
import _winreg as winreg
#start meta
__name__='web broswer helper'
__author='fffonion'
__version__=0.1
#'ENTER_explore':1
hooks={}
extra_cmd={'web':'start_webproxy','w':'start_webproxy'}
#end meta
weburl={'cn':'http://game1-cbt.ma.sdo.com:10001/connect/web/?%s',
        'cn2':'http://game2-cbt.ma.sdo.com:10001/connect/web/?%s',
        'cn3':'http://game3-cbt.ma.sdo.com:10001/connect/web/?%s',
        'tw':'http://game.ma.mobimon.com.tw:10001/connect/web/?%s'}
#other stuffs
headers={'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'X-Requested-With': 'com.square_enix.million_',
    'User-Agent': '',
    'Accept-Language': 'zh-CN, en-US',
    'Accept-Charset': 'utf-8, iso-8859-1, utf-16, *;q=0.7',}
    #'Accept-Encoding':'gzip,deflate'}
def start_webproxy(plugin_vals):
    def do(*args):
        headers['cookie']=plugin_vals['cookie']
        headers['User-Agent']=plugin_vals['poster'].header['User-Agent']
        headers['X-Requested-With']+=plugin_vals['loc']
        homeurl=weburl[plugin_vals['loc']]%(plugin_vals['cookie'].rstrip(';'))
        enable_proxy()
        print(('现在将打开浏览器窗口\n'
              '如果没有，请手动打开主页:\n'
              '%s\n'
              '对不使用IE代理的浏览器，请将代理设置为127.0.0.1:23301\n'
              '按Ctrl+C关闭并回复无代理'
            %homeurl).decode('utf-8'))
        webbrowser.open(homeurl)
        server = ThreadingHTTPServer(("", 23301) , Proxy) 
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            server.shutdown()
            disable_proxy()
    return do

def enable_proxy():
    INTERNET_SETTINGS = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
        r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
        0, winreg.KEY_ALL_ACCESS)

    winreg.SetValueEx(INTERNET_SETTINGS, 'ProxyEnable',0, winreg.REG_DWORD, 1)
    winreg.SetValueEx(INTERNET_SETTINGS, 'ProxyOverride', 0, winreg.REG_SZ, u'127.0.0.1')  # Bypass the proxy for localhost
    winreg.SetValueEx(INTERNET_SETTINGS, 'ProxyServer', 0, winreg.REG_SZ, u'127.0.0.1:23301')

def disable_proxy():
    INTERNET_SETTINGS = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
        r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
        0, winreg.KEY_ALL_ACCESS)

    winreg.SetValueEx(INTERNET_SETTINGS, 'ProxyEnable',0, winreg.REG_DWORD, 0)
    #winreg.DeleteKey(INTERNET_SETTINGS, 'ProxyOverride')
    #winreg.DeleteKey(INTERNET_SETTINGS, 'ProxyServer')
#start simplest proxy
opener =urllib2.build_opener(urllib2.ProxyHandler({}))
class Proxy(BaseHTTPRequestHandler):
    def do_GET(self):
        req=urllib2.Request(self.path,headers=headers)
        resp=opener.open(req).read()
        try:
            f = StringIO(resp)
            gzipper = gzip.GzipFile(fileobj = f)
            data = gzipper.read()
        except:
            data = resp
        self.wfile.write(data)

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):   
    #address_family = socket.AF_INET6  
    address_family = socket.AF_INET

if __name__=="__main__":
    c=start_webproxy({'cookie':'','loc':'cn'})
    c()