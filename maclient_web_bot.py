#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import gevent
import gevent.monkey
gevent.monkey.patch_all()
import time
import os
import sys
import traceback
from threading import Thread

import maclient
reload(maclient)#in case module has changed
from maclient import MAClient
from web_libs import safeeval
reload(safeeval)

from web_libs import remote_debugger
reload(remote_debugger)

mac_version = maclient.__version__
mac_web_version = 20140519.16384
maxconnected = 300

if os.name != 'nt':
    remote_debugger.listen()

class HeheError(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

class ws_keepalive(Thread):
    def __init__(self, ws):
        self.ws = ws
        Thread.__init__(self, name = 'ws_keepalive-thread')

    def run(self):
        while self.ws:
            try:
                self.ws.send("")
            except:
                break
            gevent.sleep(25)

class WebSocketBot(MAClient):
    def __init__(self, ws, serv, _hash, die_callback, born_callback):
        cfg_file = os.path.join('configs', _hash)
        if not os.path.exists(cfg_file):
            print('[new_user] hash=%s' % _hash)
            with open('config_web.ini') as inp, open(cfg_file, 'w') as out:
                out.write(inp.read())
        good = ws_keepalive(ws)
        good.start()
        self.ws = ws
        self.shellbyweb = True
        self.offline = False
        self.last_offline_keepalive_time = time.time()
        self.keep_time = 12 * 3600
        self.loginid = 0
        self.die = die_callback
        self.born = born_callback
        self.request_exit = False
        try:
            super(self.__class__, self).__init__(configfile = cfg_file, servloc = serv, savesession = False)
        except Exception as e:
            # err = traceback.format_exception(*sys.exc_info())
            # self.logpipe(err[-1])
            # self.logpipe("".join(err))
            raise e
        self.born()
        self.logger.logfile = None
        self.logger.logpipe(self.logpipe)



    def logpipe(self, _str):
        if self.shellbyweb:
            if self.ws != None or self.offline == False:
            #mac.ws == None mac.offline == False should throw a ex
                self.ws.send(_str)
            else:
                pass#sys.stdout.write(_str)

    def run(self, username, password, cmd = ''):
        self.login(username, password)
        #self.initplayer(dec)
        if cmd != '':
            self.tasker(cmd = cmd)
        else:
            self.tasker()

    #override
    def _exit(self, code):
        self.end()

    #override
    def _dopost(self, *args, **kwargs):
        if self.request_exit:
            raise HeheError('bye')
        return super(self.__class__, self)._dopost(*args, **kwargs)

    #override
    def _eval_gen(self, *args, **kwargs):
        evalstr = super(self.__class__, self)._eval_gen(*args, **kwargs)
        for s in evalstr.split('|'):
            try:
                try:
                    safeeval.check_safe_eval(s)
                except SyntaxError:
                    safeeval.check_safe_eval(evalstr)#for | in task
                    break
            except SyntaxError:
                pass
            except Exception as e:
                print
                self.logpipe("在配置文件中包含不合法的表达式 %s:\n%s: %s\n如果你认为这是误报，请联系我们\n" % (s, e.__class__.__name__, e))
                raise e
        return evalstr

    def end(self):
        # set on async exit
        self.request_exit = True
        if hasattr(self, 'player') and self.player.filedesc > 0:
            os.close(self.player.filedesc)
        #self.__class__.connected -= 1

    def cleanup(self):
        def __unrefer_all(instance):
            for n in instance.__dict__:
                setattr(instance, n, None)
        for c in self.__dict__:
            c = self.__dict__[c]
            if c.__class__.__name__ in ['player', 'card', 'item', 'boss', 'Logging']:#plugins is global
                __unrefer_all(c)
        __unrefer_all(self)
                