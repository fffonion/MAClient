#!/usr/bin/env python
# coding:utf-8
# maclient transparent proxy
# modified from sogou proxy
# Contributor:
#      fffonion        <fffonion@gmail.com>
from cross_platform import *
if PYTHON3:
    from http.server import BaseHTTPRequestHandler, HTTPServer
    from socketserver import ThreadingMixIn
    from http.client import HTTPResponse
else:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
    from SocketServer import ThreadingMixIn
    from httplib import HTTPResponse
from threading import Thread, Lock
from struct import unpack

import socket, os, select
import time, sys, random
import threading

# Minimize Memory Usage
try:
    threading.stack_size(128 * 1024)
except:
    pass
proxy_port = 23300
BufferSize = 8192
RemoteTimeout = 15

class Handler(BaseHTTPRequestHandler):
    remote = None
    # Ignore Connection Failure
    def handle(self):
        try:
            BaseHTTPRequestHandler.handle(self)
        except socket.error: pass
    def finish(self):
        try:
            BaseHTTPRequestHandler.finish(self)
        except socket.error: pass

    # CONNECT Data Transfer
    def transfer(self, a, b):
        fdset = [a, b]
        while True:
            r, w, e = select.select(fdset, [], [])
            if a in r:
                data = a.recv(BufferSize)
                if not data: break
                b.sendall(data)
            if b in r:
                data = b.recv(BufferSize)
                if not data: break
                a.sendall(data)

    def myProxy(self):
        if self.remote is None or self.lastHost != self.headers["Host"]:
            self.remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.remote.settimeout(RemoteTimeout)
            if ':' in self.headers["Host"]:
                port = int(self.headers["Host"].split(':')[1])
            else:
                port = 80
            self.remote.connect((self.headers["Host"].split(':')[0], port))
        if not self.headers['Host'].startswith('http'):self.headers['Host'] = 'http://' + self.headers['Host']

        if 'Cookie' in self.headers:
            self.sessionid = self.headers['Cookie']
            open('.session', 'w').write(self.headers['Cookie'])
            # print sessionid
        else:
            sessionid = ''

        if self.requestline.startswith('HEAD /'):  # Adjust 'HEAD /xxx' situation
            self.requestline = self.requestline.replace('HEAD ', 'HEAD ' + self.headers['Host'])
        self.remote.sendall(self.requestline.encode('ascii') + b"\r\n")
        headerstr = str(self.headers).replace("\r\n", "\n").replace("\n", "\r\n")
        self.remote.sendall(headerstr.encode('ascii', 'ignore') + b"\r\n")
        # Send Post data
        if self.command == 'POST':
            postdata = self.rfile.read(int(self.headers['Content-Length']))
            self.remote.sendall(postdata)
            # if 'cardselect/savedeckcard' in self.requestline:
            #     open('.carddeck', 'w').write(postdata)
        response = HTTPResponse(self.remote, method = self.command)
        response.begin()

        # Reply to the browser
        status = "HTTP/1.1 " + str(response.status) + " " + response.reason
        self.wfile.write(status.encode('ascii') + b'\r\n')
        hlist = []
        for line in response.msg.headers:  # Fixed multiple values of a same name
            if 'TRANSFER-ENCODING' not in line.upper():
                hlist.append(line)
        self.wfile.write("".join(hlist) + b'\r\n')

        if self.command == "CONNECT" and response.status == 200:
            return self.transfer(self.remote, self.connection)
        elif self.command == "HEAD":
            pass
        else:
            r = ''
            while True:
                response_data = response.read(BufferSize)
                if not response_data: break
                self.wfile.write(response_data)

            #            self.carddata=reponse
        # print('%s - [%s] %s "%s" %d %s' %(self.client_address[0],time.strftime('%Y-%m-%d %X',time.localtime())\
                   #  ,'',self.requestline,response.status,response.getheader('Content-length', '0')))
    do_POST = do_GET = do_CONNECT = do_HEAD = myProxy

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    # address_family = socket.AF_INET6
    address_family = socket.AF_INET

if __name__ == '__main__':
    serverport = 23300
    server_address = ("", serverport)
    server = ThreadingHTTPServer(server_address, Handler)
    # Random Target Proxy Server


    print('proxy start listening on %s' % (serverport))
    # print('-'*78)
    try:
        server.serve_forever()
    except:
        os._exit(1)
