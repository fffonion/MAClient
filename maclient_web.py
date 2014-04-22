#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import socket
import gevent
import traceback
import gevent.monkey
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
from webob import Request
import os, os.path as opath
import sys
from cross_platform import *
from maclient import MAClient
import maclient

class WebSocketBot(MAClient):
    connected = 0
    maxconnected = 233

    def __init__(self, ws, serv):
        self.cfgfile = opath.join(getPATH0, 'config_web.ini')
        MAClient.__init__(self, configfile = self.cfgfile, servloc = serv)
        self.ws = ws
        self.shellbyweb = True
        self.offline = False
        #redirect
        self.logger.logfile = None
        self.logger.logpipe(self.logpipe)
        self.last_offline_keepalive_time = time.time()
        self.__class__.connected += 1
        #Bot.__init__(self)

    def logpipe(self, _str):
        if self.shellbyweb:
            if self.ws != None or self.offline == False:
            #mac.ws == None mac.offline == False should throw a ex
                self.ws.send(_str)
            else:
                sys.stdout.write(_str)

    def run(self, username, password):
        try:
            dec = self.login(username, password)
            self.initplayer(dec)
            self.tasker('w')
        except:
            self.logpipe("".join(traceback.format_exception(*sys.exc_info())))

    def __del__(self):
        self.__class__.connected -= 1
        print "conn-1=%d" % self.connected
        self._exit(0)

offline_bots = {}
_page_cache = open(opath.join(getPATH0, "web.htm")).read()

def websocket_app(environ, start_response):

    for i in offline_bots:
        bot = offline_bots[i]
        if bot.offline == True:
            if time.time() - bot.last_offline_keepalive_time > 8:# * 3600:
                bot.offline = False

    request = Request(environ)
    if request.path == '/bot' and 'wsgi.websocket' in environ:
        ws = environ["wsgi.websocket"]
        login_id = request.GET['id']
        password = request.GET['password']
        area = request.GET.get('area', None)
        offline = request.GET.get('offline', False)
        serv = request.GET.get('serv', 'cn')
        servs = ['cn', 'cn2', 'cn3', 'jp', 'kr', 'tw', 'sg']
        if serv not in servs:
            ws.send("undefine server.\n")
            return

        if WebSocketBot.maxconnected <= WebSocketBot.connected:
            ws.send("server overload.\n")
            return

        #if offline and login_id not in config.allow_offline:
        #offline = False
        if not offline:
            ws.send("offline disable.\n")
        else:
            ws.send("offline enable.\n")

        #ws.send("http://ma.mengsky.net Nginx可能存在问题导致disconnect请更换 http://174.140.165.4:8000/\n")
        ws.send("webbot created by fffonionbinuxmengskysama\n\n")

        if login_id+password in offline_bots:
            ws.send("websocket client reconnected!\n")
            bot = offline_bots[login_id+password]
            bot.ws = ws
            bot.offline = offline
            bot.last_offline_keepalive_time = time.time()
            while True:
                gevent.sleep(60)
                try:
                    ws.send('')
                except Exception, e:
                    print 'lost websocket client keep offline work\n'
                    return

        bot = WebSocketBot(ws, serv)

        if offline:
            bot.offline = True
            offline_bots[login_id+password] = bot

        print "conn+%s=%d %s" % (environ.get('HTTP_X_REAL_IP', environ['REMOTE_ADDR']),
                                 WebSocketBot.connected, environ.get('HTTP_USER_AGENT', '-'))
        while True:
            try:
                bot.run(login_id, password)
            except (socket.error, WebSocketError), e:
                if bot.offline:
                    bot.ws = None
                    print 'lost websocket client keep offline work\n'
                    continue
                print 'lost websocket client\n'
                break
            except Exception, e:
                import traceback; traceback.print_exc()
                try:
                    bot.ws.send('%s' % e)
                except WebSocketError:
                    break
                except Exception, e:
                    print 'main loop throw a ex.!\n'
                break

        WebSocketBot.connected -= 1
        if WebSocketBot.connected < 0 and len(offline_bots)>0:
            WebSocketBot.connected = len(offline_bots)
        
        if login_id + password in offline_bots:
            print "offline bot exit. login_id=%s" % login_id
            del offline_bots[login_id+password]
        else:
            print "exit. login_id=%s" % login_id
            del bot
            #auto release del bot
    else:
        start_response("200 OK", [("Content-Type", "text/html")])
        return _page_cache.replace('[connected]', '%s' % WebSocketBot.connected).replace('[maxconnected]', '%s' % WebSocketBot.maxconnected)

if __name__ == '__main__':
    gevent.monkey.patch_all()
    if BAE:
        application = websocket_app
    else:
        if OPENSHIFT:
            ip = os.environ['OPENSHIFT_PYTHON_IP']
            port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
        else:
            ip = ""
            port = 8080
        application = gevent.pywsgi.WSGIServer((ip, port), websocket_app, handler_class=WebSocketHandler)
        application.serve_forever()