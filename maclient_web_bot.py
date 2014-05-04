#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import gevent
import gevent.monkey
gevent.monkey.patch_all()
import time
import os
from threading import Thread

import maclient
reload(maclient)#in case module has changed
from maclient import MAClient

mac_version = maclient.__version__
mac_web_version = 20140504.23333

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
        super(self.__class__, self).__init__(configfile = cfg_file, servloc = serv)
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
        self.born()
        self.logger.logfile = None
        self.logger.logpipe(self.logpipe)
        self.request_exit = False
        #Bot.__init__(self)

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
            self.tasker('w', cmd)
        else:
            self.tasker('w')

    #override
    def _exit(self, code):
        self.end()

    #override
    def _dopost(self, *args, **kwargs):
        if self.request_exit:
            raise HeheError('bye')
        return super(self.__class__, self)._dopost(*args, **kwargs)

    def end(self):
        # set on async exit
        self.request_exit = True
        if hasattr(self, 'player') and self.player.filedesc > 0:
            os.close(self.player.filedesc)
        #self.__class__.connected -= 1