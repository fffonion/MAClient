# coding:utf-8
from _prototype import plugin_prototype
import re
import sys
import time
import os, os.path as opath
from cross_platform import *
import urllib
import gzip
import threading
from xml2dict import XML2Dict
if PYTHON3:
    from io import StringIO
    import urllib.request as urllib2
else:
    from cStringIO import StringIO
    import urllib2
# start meta
__plugin_name__ = '在线升级插件'
__author = 'fffonion'
__version__ = 0.16
hooks = {}
extra_cmd = {'plugin_update':'plugin_update', 'pu':'plugin_update'}
#是否下载dev版
GET_DEV_UPDATE = True

repos = ['http://git.oschina.net/fffonion/MAClient', 'https://github.com/fffonion/MAClient']
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': 'MAClient/update v%s' % __version__,
    'X-Requested-With': 'MAClient',
    'Accept-Language': 'zh-CN, en-US',
    'Accept-Charset': 'utf-8, iso-8859-1, utf-16, *;q=0.7',
    'Accept-Encoding':'gzip'}
tolist = lambda obj:isinstance(obj, list) and obj  or [obj]

def plugin_update(plugin_vals):
    def do(args):
        if not opath.exists(opath.join(_get_temp(), '.MAClient.update')):
            check_file = opath.join(_get_temp(), '.MAClient.noupdate')
            if '-f' in args.split(' ') and opath.exists(check_file):
                os.remove(check_file)
            if not _check_update():
                print(du8('已是最新版本 (上次检查%s)\n%s' % (
                    time.strftime('%b.%d %a %H:%M', 
                        opath.exists(check_file) and \
                            time.localtime(os.path.getmtime(check_file)) or \
                            time.localtime(time.time())
                        ),
                    '' if '-f' in args.split(' ') else '可使用pu -f强制重新检查')))
                return
        _do_update()
    return do

class _bg_check(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        time.sleep(3)
        if not opath.exists(opath.join(_get_temp(), '.MAClient.update')):
            if _check_update(silent=True):
                print(du8('\n已有新版本可供升级，请输入pu或plugin_update执行更新'))

def _get_temp():
    if sys.platform == 'win32':
        return os.environ.get('tmp')
    else:
        try:
            os.listdir('/tmp')
        except OSError:
            return '.'
        else:
            return '/tmp'

def _http_get(uri, silent=False):
    if PYTHON3:
        opener = urllib2.build_opener(urllib2.ProxyHandler(urllib.request.getproxies()))
    else:
        opener = urllib2.build_opener(urllib2.ProxyHandler(urllib.getproxies()))
    for repo in repos:
        url = repo + '/raw/' + uri
        try:
            resp = opener.open(urllib2.Request(url, headers=headers), timeout = 15)
            body = resp.read()
            try:
                f = StringIO(body)
                gz = gzip.GzipFile(fileobj = f)
                body = gz.read()
            except:
                pass
        except urllib2.HTTPError as e:
            if not silent:
                print('HTTP Error %s when fetching ' + url + '' % e.code)
        except urllib2.URLError as e:
            pass
        else:
            return body

def _check_update(silent = False):
    check_file = opath.join(_get_temp(), '.MAClient.noupdate')
    if opath.exists(check_file):
        if time.time() - os.path.getmtime(check_file) < 86400:#1天内只检查一次
            return
        os.remove(check_file)
    if not silent:
        print('Retrieving meta info ...')
    body = _http_get('update/meta.xml', silent)
    if not body:
        print('Error fetching meta')
        return
    meta = XML2Dict().fromstring(body).maclient
    xml = '<?xml version="1.0" encoding="UTF-8"?><maclient><time>%d</time>' % int(time.time())
    s_update = '<update_item><name>%s</name><version>%s</version><dir>%s</dir></update_item>'
    s_new = '<new_item><name>%s</name><version>%s</version><dir>%s</dir></new_item>'
    new = False
    for k in meta.plugin + meta.script:
        script = opath.join(getPATH0, k.dir or '', k.name)
        # reserved for exe bundle
        if k.name == 'maclient.py':
            mainitm = k
        elif k.name == 'maclient_smart.py':
            smtitm = k
        if EXEBUNDLE and k.name in ['maclient_cli.py', 'maclient_smart.py']:
            continue
        if opath.exists(script):
            _s = open(script).read()
            ver = re.findall('__version__[\s=\']*([^\'\s]+)[\']*', _s)
            if ver and ver[0] < k.version:
                xml += s_update % (k.name, k.version, k.dir or '')
                new = True
        else: #new item
            xml += s_new % (k.name, k.version, k.dir or '')
            new = True
    # if EXEBUNDLE:
    #     import maclient
    #     import maclient_smart
    #     if str(maclient.__version__) < mainitm.version:
    #         xml += s_update % (mainitm.name, mainitm.version, '')
    #         new = True
    #     if str(maclient_smart.__version__) < smtitm.version:
    #         xml += s_update % (smtitm.name, smtitm.version, '')
    #         new = True
    if new:
        open(opath.join(_get_temp(), '.MAClient.update'), 'w').write(xml+'</maclient>')
        return True
    else:
        open(opath.join(_get_temp(), '.MAClient.noupdate'), 'w').write('')
        return False

def _do_update(silent = False):
    update_file = opath.join(_get_temp(), '.MAClient.update')
    try:
        _m = open(update_file).read()
    except IOError:
        return False
    if time.time() - os.path.getmtime(update_file) > 259200:#3天
        os.remove(opath.join(_get_temp(), '.MAClient.update'))
        _check_update(silent)
        return _do_update(silent)
    _top = XML2Dict().fromstring(_m).maclient
    _done = False
    update_item = 'update_item' in _top and _top.update_item or None
    new_item = 'new_item' in _top and _top.new_item or None
    for (_prompt, _meta) in [('√ 已更新 %s ↑ v%s', update_item), ('√ 新增 %s v%s', new_item)]:
        for k in tolist(_meta):
            if not k:
                continue
            if k.name == 'maclient.py':
                if not silent:
                    print(du8('√ 主程序有新版本 v%s 请至以下链接查看\n'
                              'github: https://github.com/fffonion/MAClient/\n'
                              '百度盘: http://pan.baidu.com/s/19qI4m' % k.version))
                continue
            elif k.name == 'maclient_smart.py' and EXEBUNDLE:
                new = _http_get('update/maclient_smart.bin', silent)
                try:
                    assert(new and len(new)>28000)
                    if opath.exists(opath.join(getPATH0, 'maclient_smart.py_')):
                        os.remove(opath.join(getPATH0, 'maclient_smart.py_'))
                    os.rename(opath.join(getPATH0, 'maclient_smart.pyd'),opath.join(getPATH0, 'maclient_smart.py_'))
                    open(opath.join(getPATH0, 'maclient_smart.pyd'),'wb').write(new)
                except (IOError, WindowsError, AssertionError):
                    if not silent:
                        print(du8('× maclient_smart有新版本但更新失败 v%s 请至以下链接下载完整包\n'
                              'http://pan.baidu.com/s/19qI4m' % k.version))
                else:
                    print(du8('√ 已更新 %s ↑ v%s' % (k.name, k.version)))
                continue
            new = _http_get((GET_DEV_UPDATE and 'dev/' or 'master/') + (k.dir or '') + '/' + k.name, silent)
            if not new:
                if not silent:
                    print(du8('× %s 更新失败' % k.name))
                continue
            open(opath.join(getPATH0, k.dir or '', k.name),'w').write(new.replace('\r\n', '\n'))
            if not silent:
                print(du8(_prompt % (k.name, k.version)))
                _done = True
    os.remove(update_file)
    if _done:
        print(du8('重新启动maclient以应用更新'))

#run when being imported
if opath.exists(opath.join(_get_temp(), '.MAClient.update')):
    __tip__ = '检测到更新，请输入pu或plugin_update执行更新'
else:
    b = _bg_check()
    b.setDaemon(True)
    b.start()