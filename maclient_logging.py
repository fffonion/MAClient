# coding:utf-8
import os
import sys
import time
import locale
import logging
import logging.handlers
from cross_platform import *

convstr = (sys.platform.startswith('cli') or PYTHON3 or NICE_TERM)and \
        (lambda str: str) or \
        (lambda str: str.decode('utf-8').encode(locale.getdefaultlocale()[1] or 'utf-8', 'replace'))

class Logging(type(sys)):
    # paste from goagent
    CRITICAL = 5
    FATAL = CRITICAL
    ERROR = 4
    WARNING = 3
    WARN = WARNING
    INFO = 2
    SLEEP = INFO
    DEBUG = 1
    NOTSET = 0
    def __init__(self, *args, **kwargs):
        self.level = self.__class__.INFO
        self.__write = __write = sys.stdout.write
        self.isatty = getattr(sys.stdout, 'isatty', lambda: False)()
        self.__set_error_color = lambda: None
        self.__set_warning_color = lambda: None
        self.__set_debug_color = lambda: None
        self.__set_sleep_color = lambda: None
        self.__reset_color = lambda: None
        if self.isatty:
            if os.name == 'nt':
                import ctypes
                SetConsoleTextAttribute = ctypes.windll.kernel32.SetConsoleTextAttribute
                GetStdHandle = ctypes.windll.kernel32.GetStdHandle
                self.__set_error_color = lambda: SetConsoleTextAttribute(GetStdHandle(-11), 0x0C)
                self.__set_warning_color = lambda: SetConsoleTextAttribute(GetStdHandle(-11), 0x06)
                self.__set_debug_color = lambda: SetConsoleTextAttribute(GetStdHandle(-11), 0x02)
                self.__set_sleep_color = lambda: SetConsoleTextAttribute(GetStdHandle(-11), 0x08)
                self.__set_bright_color = lambda: SetConsoleTextAttribute(GetStdHandle(-11), 0x0F)
                self.__reset_color = lambda: SetConsoleTextAttribute(GetStdHandle(-11), 0x07)
            elif os.name == 'posix':
                self.__set_error_color = lambda: __write('\033[31m')
                self.__set_warning_color = lambda: __write('\033[33m')
                self.__set_debug_color = lambda: __write('\033[32m')
                self.__set_sleep_color = lambda: __write('\033[36m')
                self.__set_bright_color = lambda: __write('\033[32m')
                self.__reset_color = lambda: __write('\033[0m')
        self.logfile = None
 
    def setlogfile(self, f):
        self.logfile = open(f, 'a')

    @classmethod
    def getLogger(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def basicConfig(self, *args, **kwargs):
        self.level = int(kwargs.get('level', self.__class__.INFO))
        if self.level > self.__class__.DEBUG:
            self.debug = self.dummy

    def log(self, level, fmt, *args, **kwargs):
        # fmt=du8(fmt)
        try:
            self.__write(convstr(du8('%-5s - [%s] %s\n' % (level, time.strftime('%X', time.localtime()), fmt % args))))
        except TypeError:
            fmt = fmt.replace('%','%%')
            self.__write(convstr(du8('%-5s - [%s] %s\n' % (level, time.strftime('%X', time.localtime()), fmt % args))))
        #sys.stdout.flush()
        return '[%s] %s\n' % (time.strftime('%b %d %X', time.localtime()), fmt % args)

    def mac_log(self, mac, level, fmt, *args, **kwargs):
        # fmt=du8(fmt)
        _str = du8('%-5s - [%s] %s\n' % (level, time.strftime('%X', time.localtime()), fmt % args))
        if mac.shellbyweb:
            if mac.ws != None or mac.offline == False:
                #mac.ws == None mac.offline == False should throw a ex
                mac.ws.send(_str)
        else:
            self.__write(convstr(_str))
        #self.__write(convstr(_str))
        return '[%s] %s\n' % (time.strftime('%b %d %X', time.localtime()), fmt % args)

    def dummy(self, *args, **kwargs):
        pass

    def debug(self, fmt, *args, **kwargs):
        self.__set_debug_color()
        self.log('DEBUG', fmt, *args, **kwargs)
        self.__reset_color()

    def mac_info(self, mac, fmt, *args, **kwargs):
        puretext = self.mac_log(mac, 'INFO', fmt, *args)
        if self.logfile:
            self.logfile.write(puretext)

    def info(self, fmt, *args, **kwargs):
        puretext = self.log('INFO', fmt, *args)
        if self.logfile:
            self.logfile.write(puretext)

    def mac_sleep(self, mac, fmt, *args, **kwargs):
        self.__set_sleep_color()
        self.mac_log(mac, 'SLEEP', fmt, *args, **kwargs)
        self.__reset_color()

    def sleep(self, fmt, *args, **kwargs):
        self.__set_sleep_color()
        self.log('SLEEP', fmt, *args, **kwargs)
        self.__reset_color()

    def warning(self, fmt, *args, **kwargs):
        self.__set_warning_color()
        self.log('WARNING', fmt, *args, **kwargs)
        self.__reset_color()

    def warn(self, fmt, *args, **kwargs):
        self.warning(fmt, *args, **kwargs)

    def error(self, fmt, *args, **kwargs):
        self.__set_error_color()
        self.log('ERROR', fmt, *args, **kwargs)
        self.__reset_color()

    def mac_error(self, mac, fmt, *args, **kwargs):
        self.__set_error_color()
        self.mac_log(mac, 'ERROR', fmt, *args, **kwargs)
        self.__reset_color()

    def exception(self, fmt, *args, **kwargs):
        self.error(fmt, *args, **kwargs)
        traceback.print_exc(file = sys.stderr)

    def critical(self, fmt, *args, **kwargs):
        self.__set_error_color()
        self.log('CRITICAL', fmt, *args, **kwargs)
        self.__reset_color()
