#!/usr/bin/python
# -*- coding: utf-8 -*-
# if 'threading' in sys.modules:
import gevent
import gevent.monkey
gevent.monkey.patch_all()
import time
import socket
from threading import Thread
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
from webob import Request
from cross_platform import *
import sys

from maclient import MAClient
import maclient
from datetime import datetime, timedelta, tzinfo

class zh_BJ(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours = 8)
    def dst(self, dt):
        return timedelta(0)

startup_time = datetime.now(zh_BJ()).strftime('%m.%d %H:%M:%S')
_index_cache = open("web.htm").read().replace('[startup_time]', startup_time)\
                .replace('[version_str]', str(maclient.__version__))

reload(sys)
sys.setdefaultencoding('utf-8')
class HeheError(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

class WebSocketBot(MAClient):
    connected = 0
    maxconnected = 333

    def __init__(self, ws, serv):
        MAClient.__init__(self, configfile = 'config_web.ini', servloc = serv)
        self.ws = ws
        self.shellbyweb = True
        self.offline = False
        self.last_offline_keepalive_time = time.time()
        self.keep_time = 12 * 3600
        self.loginid = 0
        self.__class__.connected += 1
        self.logger.logfile = None
        self.logger.logpipe(self.logpipe)
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

    def _exit(self, code):
        self.end()

    def end(self):
        if self.player.filedesc > 0:
            os.close(self.player.filedesc)
        self.__class__.connected -= 1
        print "conn-1=%d" % self.connected
        raise HeheError('hehe')#self._exit(0)

offline_bots = {}

class cleanup(Thread):
    def __init__(self):
        Thread.__init__(self, name = 'cleanup-thread')

    def run(self):
        while True:
            for i in offline_bots:
                bot = offline_bots[i]
                if not bot.offline:
                    continue
                #if bot.offline == True:
                if time.time() - bot.last_offline_keepalive_time > bot.keep_time:
                    try:
                        bot.end()
                    except:
                        pass
            gevent.sleep(60)

def websocket_app(environ, start_response):
    #cleanup()
    request = Request(environ)
    if request.path == '/bot' and 'wsgi.websocket' in environ:
        ws = environ["wsgi.websocket"]
        login_id = request.GET['id']
        password = request.GET['password']
        area = request.GET.get('area', None)
        offline = request.GET.get('offline', False)
        keep_time = int(request.GET.get('keep_time', 12 * 3600))
        cmd = request.GET.get('cmd', '')
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
            ws.send("离线模式已经禁用,系统会在你关闭浏览器后停止挂机\n")
        else:
            ws.send("离线模式已经启用,系统会代挂N小时.\n")

        ws.send("webbot created by fffonionbinuxmengskysama\n\n")

        #reconnects
        if login_id+password in offline_bots:
            ws.send("websocket client reconnected!\n")
            bot = offline_bots[login_id+password]
            bot.offline = offline
            bot.ws = ws
            bot.keep_time = keep_time
            bot.last_offline_keepalive_time = time.time()
            while True:
                gevent.sleep(60)
                try:
                    ws.send('')
                    #cleanup()
                except Exception, e:
                    print '[%s]login_id=%s client keep offline = %swork\n' % (e, login_id, offline)
                    return
        #new
        bot = WebSocketBot(ws, serv)
        bot.loginid = login_id

        if offline:
            bot.keep_time = keep_time
            bot.last_offline_keepalive_time = time.time()
            bot.offline = True
            offline_bots[login_id+password] = bot

        print "conn+%s=%d %s" % (environ.get('HTTP_X_REAL_IP', environ['REMOTE_ADDR']),
                                 WebSocketBot.connected, environ.get('HTTP_USER_AGENT', '-'))

        print "login id=%s" % login_id

        while True:
            try:
                bot.run(login_id, password, cmd)
            except (socket.error, WebSocketError), e:
                #import traceback; traceback.print_exc()
                if bot.offline:
                    bot.ws = None
                    print '[%s]id = %s keep offline work\n' % (e, login_id)
                    continue
                print '[%s]id = %s exit bot\n' % (e, login_id)
                break
            except HeheError:#hehe
                print 'id = %s force exit.' % login_id
                break
            except Exception, e:
                print 'id = %s except offline=%s' % (login_id, offline)
                import traceback; traceback.print_exc(limit = 2)
                if not bot.offline:
                    break
                try:
                    bot.ws.send("".join(traceback.format_exception(*sys.exc_info())))
                except WebSocketError:
                    pass
                except Exception, e:
                    print 'main loop throw a ex.!\n'
                break

        if login_id+password in offline_bots:
            bot = offline_bots.pop(login_id+password)
            print "offline bot exit. login_id=%s" % login_id
        else:
            print "exit. login_id=%s" % login_id
        try:
            bot.end()
        except HeheError:
            pass
        #auto release del bot
    else:
        start_response("200 OK", [("Content-Type", "text/html")])
        ol = WebSocketBot.connected# + 169
        return _index_cache.replace('[connected]', '%d/%d' % (ol, len(offline_bots))).replace('[maxconnected]', '%s' % WebSocketBot.maxconnected)

if __name__ == '__main__':
    cleanup().start()
    server = gevent.pywsgi.WSGIServer(("", 8000), websocket_app, handler_class=WebSocketHandler)
    server.serve_forever()
