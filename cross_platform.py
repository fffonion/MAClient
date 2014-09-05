#!/usr/bin/env python
# coding:utf-8
# maclient compatibility tool
# Contributor:
#      fffonion        <fffonion@gmail.com>
import os
import os.path as opath
import sys
import locale
PYTHON3 = sys.version.startswith('3')
IRONPYTHON = sys.platform == 'cli'
EXEBUNDLE = opath.split(sys.argv[0])[1].find('py') == -1
LOCALE = locale.getdefaultlocale()[0]
CODEPAGE = locale.getdefaultlocale()[1]
NICE_TERM = 'NICE_TERM' in os.environ
ANDROID = 'ANDROID_ARGUMENT' in os.environ
convhans = lambda x:x
try:
    import ZhConversion
except ImportError:
    pass
else:
    chans = ZhConversion.convHans()
    if LOCALE == 'zh_TW':
        convhans = chans.toTW
    elif LOCALE == 'zh_HK':
        convhans = chans.toHK
if PYTHON3:
    import imp
    reload = imp.reload
    xrange = range


getPATH0 = (not EXEBUNDLE or IRONPYTHON) and \
     (PYTHON3 and \
        sys.path[0]  # python3
        or sys.path[0].decode(sys.getfilesystemencoding())
     ) \
     or sys.path[1].decode(sys.getfilesystemencoding())  # pyinstaller build

if ANDROID:
    sys.path.insert(0, opath.join(getPATH0, 'modules.zip'))
    
raw_du8 = (IRONPYTHON or PYTHON3) and \
    (lambda str:str) or \
    (lambda str:convhans(str).decode('utf-8'))

safestr = (sys.platform.startswith('cli') or PYTHON3 or NICE_TERM)and \
        (lambda str: str) or \
        (lambda str: str.decode('utf-8').encode(locale.getdefaultlocale()[1] or 'utf-8', 'replace'))

du8 = lambda x: safestr(raw_du8(x))

raw_inputd = PYTHON3 and \
        (lambda s:input(s)) \
    or \
        (lambda s:raw_input(raw_du8(s).encode(CODEPAGE or 'utf-8')).decode(CODEPAGE or 'utf-8').encode('utf-8'))
        
# from goagent.appcfg
def _win_getpass(prompt='Password:', stream=None):
    password = ''
    sys.stdout.write(prompt)
    while 1:
        ch = msvcrt.getch()
        if ch == '\b':
            if password:
                password = password[:-1]
                sys.stdout.write('\b \b')
            else:
                continue
        elif ch == '\r':
            sys.stdout.write(os.linesep)
            return password
        else:
            password += ch
            sys.stdout.write('*')

try:
    import msvcrt
    getpass = _win_getpass
except ImportError:
    import getpass
    getpass = getpass.getpass

wsa_errors = None
if sys.platform.startswith('win'):
    wsa_errors = {
        10004:'中断函数调用',
        10013:'权限被拒绝',
        10014:'错误的地址',
        10022:'参数无效',
        10024:'打开的文件太多',
        10035:'资源暂时不可用',
        10036:'现在正在进行的操作',
        10037:'操作已在进行',
        10038:'套接字操作非插座进行插座上的',
        10039:'所需的目标地址',
        10040:'消息太长',
        10041:'协议的套接字类型不正确',
        10042:'错误的协议选项',
        10043:'不支持的协议',
        10044:'套接字类型不受支持',
        10045:'不支持此操作',
        10046:'协议系列不支持',
        10047:'系列协议系列不支持地址',
        10048:'地址已在使用中',
        10049:'无法分配请求的地址',
        10050:'网络出现故障',
        10051:'网络不可访问',
        10052:'网络中断连接重置',
        10053:'软件造成连接终止',
        10054:'连接被对等方重置',
        10055:'没有可用的缓冲区空间',
        10056:'套接字已连接',
        10057:'套接字未连接',
        10058:'套接字关闭后无法发送',
        10060:'连接已超时',
        10061:'连接被拒绝',
        10064:'主机已关闭',
        10065:'没有到主机的路由',
        10067:'进程太多。',
        10091:'网络子系统不可用。',
        10092:'超出范围的 Winsock.dll 版本',
        10093:'还没有执行成功的 WSAStartup',
        10101:'正在进行的正常关机',
        10109:'类找不到类型',
        11001:'找不到主机。没有此主机不存在。',
        11002:'没有发现非权威主机',
        11003:'这是一个不可恢复的错误。',
        11004:'有效的名称、 请求类型的任何数据记录'
    }


def try_load_native(mod_name):#little hack on normal import routine
    if mod_name in sys.modules:
        return sys.modules[mod_name]
    android_internal_mod_name = '/data/data/com.hipipal.qpyplus/files/lib/python2.7/site-packages/%s.so' % mod_name
    #copy new files if has former library is in internal storage
    # if ANDROID and opath.exists(android_internal_mod_name) and opath.exists('%s.so' % mod_name) and \
    #         os.stat('%s.so' % mod_name).st_mtime > os.stat(android_internal_mod_name).st_mtime:
    #     with open(android_internal_mod_name, 'wb') as f:
    #         f.write(open('%s.so' % mod_name, 'rb').read())
    try:
        mod = __import__(mod_name)
    except ImportError as ex:
        if str(ex).find('failed to map segment') and ANDROID:#try to link library in noexec dir
            mod_dir = '.'
            if not opath.exists(opath.join('.', '%s.so' % mod_name)):
                mod_dir = os.environ['PYTHONPATH'].split(':')[-1]#fix path when import is naked(comes with initial)
            # python seems to load module in the same directory first, so if we failed here,
            # we can assume that this a newer native library in (noexec) sdcard
            with open(android_internal_mod_name, 'wb') as f:
                f.write(open(opath.join(mod_dir, '%s.so' % mod_name), 'rb').read())
            if opath.exists(opath.join(mod_dir, '%s.s_' % mod_name)):
                os.remove(opath.join(mod_dir, '%s.s_' % mod_name))
            os.rename(opath.join(mod_dir, '%s.so' % mod_name), opath.join(mod_dir, '%s.s_' % mod_name))
            mod = __import__(mod_name) #throw exception now, it's the library problem
        else:
            raise ImportError(str(ex))
    #globals()[mod_name] = mod
    return mod