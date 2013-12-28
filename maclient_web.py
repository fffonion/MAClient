#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import socket
import gevent
import gevent.monkey
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
from webob import Request
from cross_platform import *

from maclient import maClient
import maclient

class WebSocketBot(maClient):
    connected = 0
    maxconnected = 233

    def __init__(self, ws, serv):
        maClient.__init__(self, configfile = 'config_web.ini', servloc = serv)
        self.ws = ws
        self.shellbyweb = True
        self.offline = False
        self.last_offline_keepalive_time = time.time()
        self.__class__.connected += 1
        #Bot.__init__(self)

    def run(self, username, password):
        dec = self.login(username, password)
        self.initplayer(dec)
        self.tasker('w')

    def __del__(self):
        self.__class__.connected -= 1
        print "conn-1=%d" % self.connected

offline_bots = {}

def websocket_app(environ, start_response):

    for i in offline_bots:
        bot = offline_bots[i]
        if bot.offline == True:
            if time.time() - bot.last_offline_keepalive_time > 8 * 3600:
                bot.offline = False

    request = Request(environ)
    if request.path == '/bot' and 'wsgi.websocket' in environ:
        ws = environ["wsgi.websocket"]
        login_id = request.GET['id']
        password = request.GET['password']
        area = request.GET.get('area', None)
        offline = request.GET.get('offline', False)
        serv = request.GET.get('serv', 'cn')
        servs = ['cn', 'cn1', 'cn2', 'jp', 'kr', 'tw']
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

        ws.send("http://ma.mengsky.net Nginx可能存在问题导致disconnect请更换 http://174.140.165.4:8000/\nwebbot created by fffonionbinuxmengskysama\n\n")

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
                except WebSocketError:
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

        if login_id+password in offline_bots:
            print "offline bot exit. login_id=%s" % login_id
            del offline_bots[login_id+password]
        else:
            print "exit. login_id=%s" % login_id
            #auto release del bot
    else:
        start_response("200 OK", [("Content-Type", "text/html")])
        return open("web.htm").read().replace('[connected]', '%s' % WebSocketBot.connected).replace('[maxconnected]', '%s' % WebSocketBot.maxconnected)

if __name__ == '__main__':
    gevent.monkey.patch_all()
    server = gevent.pywsgi.WSGIServer(("", 8000), websocket_app, handler_class=WebSocketHandler)
    server.serve_forever()