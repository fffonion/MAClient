#!/usr/bin/python
# -*- coding: utf-8 -*-
import time

import maclient
reload(maclient)#in case module has changed
from maclient import MAClient
mac_version = maclient.__version__

class HeheError(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)
        
class WebSocketBot(MAClient):

    def __init__(self, ws, serv, die_callback, born_callback):
        MAClient.__init__(self, configfile = 'config_web.ini', servloc = serv)
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
        return MAClient._dopost(self, *args, **kwargs)

    def end(self):
        # set on async exit
        self.request_exit = True
        if self.player.filedesc > 0:
            os.close(self.player.filedesc)
        #self.__class__.connected -= 1