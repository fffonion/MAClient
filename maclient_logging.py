# coding:utf-8
import os
import sys
from datetime import datetime, tzinfo, timedelta
import locale
import logging
import logging.handlers
from cross_platform import *

class zh_BJ(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours = 8)
    def dst(self, dt):
        return timedelta(0)


class Logging(object):
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
        self.__write = __write = lambda x:sys.stdout.write(safestr(x))
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

    def logpipe(self, to):
        self.__write = to

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
            self.__write(raw_du8('%-5s - [%s] %s\n' % (level, datetime.now(zh_BJ()).strftime('%X'), fmt % args)))
        except ValueError:
            fmt = fmt.replace('%','%%')
            self.__write(raw_du8('%-5s - [%s] %s\n' % (level, datetime.now(zh_BJ()).strftime('%X'), fmt % args)))
        #sys.stdout.flush()
        return '[%s] %s\n' % (datetime.now(zh_BJ()).strftime('%b %d %X'), fmt % args)

    def dummy(self, *args, **kwargs):
        pass

    def debug(self, fmt, *args, **kwargs):
        self.__set_debug_color()
        self.log('DEBUG', fmt, *args, **kwargs)
        self.__reset_color()

    def info(self, fmt, *args, **kwargs):
        puretext = self.log('INFO', fmt, *args)
        if self.logfile:
            self.logfile.write(puretext)

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

    def exception(self, fmt, *args, **kwargs):
        self.error(fmt, *args, **kwargs)
        traceback.print_exc(file = sys.stderr)

    def critical(self, fmt, *args, **kwargs):
        self.__set_error_color()
        self.log('CRITICAL', fmt, *args, **kwargs)
        self.__reset_color()
