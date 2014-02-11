# coding:utf-8
from __future__ import print_function
from _prototype import plugin_prototype
from cross_platform import *
import datetime
import sys
import time
# start meta
__plugin_name__ = '没节操的过年插件'
__author = 'fffonion'
__version__ = 0.1
hooks = {}
# extra cmd hook
extra_cmd = {}
# end meta
if (datetime.date.today().day >=30 and datetime.date.today().month==1) or (datetime.date.today().day<=1 and datetime.date.today().month==2):
    if getattr(sys.stderr, 'isatty', lambda: False)():
        if os.name == 'nt':
            import ctypes
            SetConsoleTextAttribute = ctypes.windll.kernel32.SetConsoleTextAttribute
            GetStdHandle = ctypes.windll.kernel32.GetStdHandle
            pprint = lambda: SetConsoleTextAttribute(GetStdHandle(-11), 0x0C)
            pprint2 = lambda: SetConsoleTextAttribute(GetStdHandle(-11), 0x0E)
            pprint3 = lambda: SetConsoleTextAttribute(GetStdHandle(-11), 0x0A)
            reset_color = lambda: SetConsoleTextAttribute(GetStdHandle(-11), 0x07)
        elif os.name == 'posix':
            __write = sys.stderr.write
            pprint = lambda: __write('\033[31m')
            reset_color = lambda: __write('\033[0m')
            pprint2 = lambda: __write('\033[33m')
            pprint3 = lambda: __write('\033[32m')
    print('''                                 .''.
       .''.             *''*    :_\/_:     . 
      :_\/_:   .    .:.*_\/_*   : /\ :  .'.:.'.''',end='')
    pprint()
    print(du8('     马年快乐！').center(10))
    reset_color()
    print('''  .''.: /\ : _\(/_  ':'* /\ *  : '..'.  -=:o:=-
 :_\/_:'.:::. /)\*''*  .|.* '.\'/.'_\(/_'.':'.''',end='')
    pprint2()
    print(du8('     这里有我顶着~\(≧▽≦)/~'))
    reset_color()
    print(''' : /\ : :::::  '*_\/_* | |  -= o =- /)\    '  *
  '..'  ':::'   * /\ * |'|  .'/.\'.  '._____''',end='')
    pprint3()
    if datetime.date.today().day ==31 or datetime.date.today().day==1:
         print(du8(' '*15+'快去串门吧'))
    else:
        print(du8(' '*10+'快去吃年夜饭吧'))
    reset_color()
    print('''      *        __*..* |  |     :      |.   |' .---"|
       _*   .-'   '-. |  |     .--'|  ||   | _|    |
    .-'|  _.|  |    ||   '-__  |   |  |    ||      |
    |' | |.    |    ||       | |   |  |    ||      |
 ___|  '-'     '    ""       '-'   '-.'    '`      |____
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~''')# originally from http://www.geocities.com/spunk1111/july4.htm#fireworks
    time.sleep(2.5)