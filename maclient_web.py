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
from hashlib import md5
from binascii import hexlify
import os, os.path as opath
import sys
import json
from threading import Thread
from cross_platform import *
from maclient import MAClient
import maclient
class OutputModel:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError()

    def send(self, payload):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()

class WebSocket(OutputModel):
    def __init__(self, environ):
        self.conn = environ["wsgi.websocket"]

    def send(self, payload):
        self.conn.send(payload)

    def close(self):
        self.conn.close()

class SaeChannel(OutputModel):
    def __init__(self, name, duration = 60):
        from sae import channel
        self.name = name
        self.client_url = channel.create_channel(name, duration)
        self.send = lambda x:x#lambda d:channel.send_message(name, d)

    def close(self):
        pass

class LongPolling(OutputModel):
    pass

class JsonMsgModel:
    ERR_SERVER_LOC_UNDEFINED = 10001
    ERR_SERVER_OVERLOAD = 10002
    ERR_RUNTIME_ERROR = 10000
    ERR_NO_SUCH_USER = 10003

    @classmethod
    def error(s, code, msg):
        return json.dumps({'code':code, 'errmsg':msg, 'data':None})

    @classmethod
    def message(s, msg):
        return json.dumps({'code':0, 'errmsg':None, 'data':msg})

class Bot(MAClient):
    connected = 0
    maxconnected = 233

    def __init__(self, out, serv, uid, pwd):
        self.cfgfile = opath.join(getPATH0, 'config_web.ini')
        MAClient.__init__(self, configfile = self.cfgfile, servloc = serv)
        self.out = out
        self.uid, self.pwd = uid, pwd
        self.shellbyweb = True
        self.offline = False
        self.running = True
        #redirect
        self.logger.logfile = None
        self.logger.logpipe(self.logpipe)
        self.last_offline_keepalive_time = time.time()
        self.__class__.connected += 1
        #Bot.__init__(self)

    def logpipe(self, _str):
        if self.shellbyweb:
            if self.out != None or self.offline == False:
            #mac.ws == None mac.offline == False should throw a ex
                self.out.send(_str)
            else:
                sys.stdout.write(_str)

    def run(self):
        dec = self.login(self.uid, self.pwd)
        self.initplayer(dec)
        self.tasker('w')

    def end(self):
        self.__class__.connected -= 1
        print "conn-1=%d" % self.connected
        if self.__class__.connected < len(offline_botruns):
            self.__class__.connected = len(offline_botruns)
        self.running = False
        self._exit(0)

class __Bot():
    connected = 0
    maxconnected = 233
    def __init__(self, out, serv):
        pass

    def run(self, username, password):
        while True:
            gevent.sleep(30)
        print username,'exit' 

    def __del__(self):
        self.__class__.connected -= 1
        print "conn-1=%d" % self.connected
        if self.__class__.connected < len(offline_botruns):
            self.__class__.connected = len(offline_botruns)

class BotRunner(Thread):
    def __init__(self, bot):
        self.bot = bot
        Thread.__init__(self)

    def run(self):
        while self.bot and self.bot.running:
            try:
                self.bot.run()
            except (socket.error, WebSocketError), e:
                if self.bot.offline:
                    self.bot.out = None
                    print 'lost websocket client keep offline work'
                    continue
                print 'lost websocket client'
                break
            except Exception, e:
                import traceback
                traceback.print_exc()
                try:
                    self.bot.out.send("".join(traceback.format_exception(*sys.exc_info())))
                except WebSocketError:
                    pass
                except Exception, e:
                    print 'main loop throws a ex.!'
                break
        self.bot.end()

offline_botruns = {}
_page_cache = open(opath.join(getPATH0, "web.htm")).read()


def application(environ, start_response):
    jsonret = lambda data:(start_response("200 OK", [("Content-Type", "application/json")]), data)[1]

    for i in offline_botruns:
        if not hasattr(offline_botruns[i], 'bot'):#pending stop
            continue
        bot = offline_botruns[i].bot
        if bot.offline == True:
            if time.time() - bot.last_offline_keepalive_time > 8:# * 3600:
                bot.offline = False
    request = Request(environ)
    if request.path == '/bot':
        WEBSOCKET = 'wsgi.websocket' in environ
        login_id = request.GET['id']
        password = request.GET['password']
        _key = md5(login_id + password).hexdigest()
        _key_int = hexlify(_key)
        area = request.GET.get('area', None)
        offline = request.GET.get('offline', False)
        logout = request.GET.get('logout', False)
        serv = request.GET.get('serv', 'cn')
        servs = ['cn', 'cn2', 'cn3', 'jp', 'kr', 'tw', 'sg']
        if WEBSOCKET:
            out = environ["wsgi.websocket"]
        elif SAE:
            out = SaeChannel(_key)

        if serv not in servs:
            return jsonret(JsonMsgModel.error(JsonMsgModel.ERR_SERVER_LOC_UNDEFINED, "undefine server."))

        if Bot.maxconnected <= Bot.connected:
            return jsonret(JsonMsgModel.error(JsonMsgModel.ERR_SERVER_OVERLOAD, "server overload."))
        if logout:
            if _key_int in offline_botruns:
                print "wait for exit"
                offline_botruns[_key_int].bot.end()
                offline_botruns[_key_int].join()
                del offline_botruns[_key_int]
                print "offline bot exit. login_id=%s" % login_id
                return jsonret(JsonMsgModel.message('logout succeed.'))
            else:
                return jsonret(JsonMsgModel.error(JsonMsgModel.ERR_NO_SUCH_USER, "no such user."))
        #if offline and login_id not in config.allow_offline:
        #offline = False
        if not offline:
            out.send("offline disable.\n")
        else:
            out.send("offline enable.\n")

        #out.send("http://ma.mengsky.net Nginx可能存在问题导致disconnect请更换 http://174.140.165.4:8000/\n")
        out.send("webbot created by fffonionbinuxmengskysama\n\n")
        b=time.time()
        if _key_int in offline_botruns:
            out.send("client reconnected!\n")
            bot = offline_botruns[_key_int].bot
            bot.out = out
            bot.offline = offline
            bot.last_offline_keepalive_time = time.time()
            if WEBSOCKET:
                while True:
                    gevent.sleep(60)
                    try:
                        out.send('')
                    except Exception, e:
                        print 'lost connection, client keep offline work\n'
                        return
            elif SAE:
                return jsonret(JsonMsgModel.message({'channel_url':out.client_url, 'reconnected':1}))
        #是新用户
        #
        bot = Bot(out, serv, login_id, password)
        #bot.run()
        botrun = BotRunner(bot)
        botrun.start()
        if offline:
            bot.offline = True
            offline_botruns[_key_int] = botrun
        print "conn+%s=%d %s" % (environ.get('HTTP_X_REAL_IP', environ['REMOTE_ADDR']),
                     Bot.connected, environ.get('HTTP_USER_AGENT', '-'))
        if WEBSOCKET:
            botrun.join()#如果现在退出ws会被关闭
        if SAE:
            return jsonret(JsonMsgModel.message({'channel_url':out.client_url, 'new':1}))
        #auto release del bot
    elif request.path == '/ajax':
        cmd = request.GET['cmd']
        if cmd == 'load':
            return jsonret(JsonMsgModel.message({'connected':Bot.connected, 'maxconnected':Bot.maxconnected}))
        elif cmd == 'users':
            return jsonret(JsonMsgModel.message(offline_botruns.keys()))
        elif cmd == 'dump':
            a=dict(globals())
            a.update(locals())
            return jsonret(JsonMsgModel.message(a[request.GET['name']]))
    else:
        start_response("200 OK", [("Content-Type", "text/html")])
        return _page_cache.replace('[connected]', '%s' % Bot.connected).replace('[maxconnected]', '%s' % Bot.maxconnected)

gevent.monkey.patch_all()

if not (BAE or SAE):
    if OPENSHIFT:
        ip = os.environ['OPENSHIFT_PYTHON_IP']
        port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
    else:
        ip = ""
        port = 8080
    server = gevent.pywsgi.WSGIServer((ip, port), application, handler_class=WebSocketHandler)
    server.serve_forever()