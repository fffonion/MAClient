#!/usr/bin/env python
# coding:utf-8
# you know
# Contributor:
#      fffonion        <fffonion@gmail.com>
from _prototype import plugin_prototype
import random
import time
import sys
import os
import sys
import string
from threading import Thread, RLock
from cross_platform import *
import maclient_network
from maclient import MAClient
__plugin_name__ = 'unlimited bc works'
__author = 'fffonion'
__version__ = 0.01
hooks = {'ENTER__use_item':9}
extra_cmd = {}

if PYTHON3:
    _split = lambda x, y = ',':list(map(lambda x:x.decode('utf-8'), x.encode(encoding = 'utf-8').split(y.encode('utf-8'))))
    map = lambda *args, **kwargs:list(map(*args, **kwargs))
else:
    _split = lambda x, y = ',':x.split(y)

TYPE_AP, TYPE_BC = 0, 1

class Servant(MAClient):
    def __init__(self, master, *args, **kwargs):
        MAClient.__init__(self, *args, **kwargs)
        self.master = master

    def bind_contract(self):
        # 和我签订契约 成为小号王吧
        param = 'dialog=1&user_id=%s' % self.master.player.id
        resp, ct = self._dopost('friend/add_friend', postdata = param)
        return not resp['error']

    def end_contract(self, uid):
        param = 'dialog=1&user_id=%s' % self.master.player.id
        resp, ct = self._dopost('friend/remove_friend', postdata = param)
        return not resp['error']

class ServantPool(Thread):
    def __init__(self, master, servant_count = 10):
        Thread.__init__(self, name = 'UBW-servant')
        self.servant_accounts = {}
        self.available_accounts = []
        self.servant_count = servant_count
        self.master = master
        self.end_of_war = False
        self.check_reg_tool()
        self.load_servant_accounts()
        self.lock = RLock()

    def check_reg_tool(self):
        if 'reg_gen' in self.master.plugin.plugins and self.master.plugin._get_module_meta('reg_gen', '__version__') < 0.35:
            self.master.logger.error('reg_gen 插件不存在或版本过旧，ubw无法启动')
            self.end_of_war = True

    def load_servant_accounts(self):
        if os.path.exists('ubw_accounts.txt'):
            for l in open('ubw_accounts.txt').readlines():
                l = l.rstri('\n').rstrip('\r').split(' ')
                tm = [0, 2] if len(l) == 2 else map(int, l[2:4])
                self.servant_accounts[' '.join(l[:2])] = tm
                if (time.time() - tm[0] > 86400) and tm[1] > 0:
                    self.available_accounts.append(' '.join(l[:2]))
            self.master.logger.debug('ubw:loaded %d, %d available' % (len(self.servant_accounts), len(self.available_accounts)))

    def save_servant_accounts(self):
        with open('ubw_accounts.txt', 'w') as f:
            for p in self.servant_accounts:
                f.write('%s %d\n' % (p, self.servant_accounts[f]))

    def new_servant(self):
        self.master.tasker(cmd = 'reg -233')
        try:
            uname_pwd = open('.ubw.account.new.txt').read()
            self.servant_accounts[uname_pwd] = [0, 2]
            self.available_accounts.append(uname_pwd)
        except Exception as ex:
            self.master.logger.warning('ubw:regist error')

    def run(self):
        cnt = 0
        while not self.end_of_war:
            if len(self.available_accounts) < self.servant_accounts:#fill it up
                self.lock.acquire()
                self.new_servant()
                self.lock.release()
            time.sleep(30)
            cnt += 1
            if cnt == 10:#every 5 min
                self.save_servant_accounts()
                cnt = 0
        self.save_servant_accounts()

    def summon_servant(self):
        self.lock.acquire()
        if len(self.available_accounts) == 0:
            self.new_servant()
        _ = random.randrange(len(self.available_accounts))
        _key = self.available_accounts(_)
        last_time, count = self.servant_accounts(_key)
        count -= 1
        if count == 0:
            self.available_accounts.pop(_)
        self.servant_accounts[_key] = [int(time.time()), count]
        self.lock.release()
        u, p = _key.split(' ')
        s = Servant(master)
        s.login(u, p)
        return s

class plugin(plugin_prototype):
    def __init__(self):
        self.not_compatible = False
        self.servant_pool_initialized = False

    def excalibur(self, mac, type = TYPE_BC):
        # 添加servant
        servant = self.servant_pool.summon_servant()
        # servant 上线
        servant.bind_contract()
        # master签订契约
        time.sleep(1.618)
        param = 'dialog=1&user_id=%s' % servant.player.id
        resp, ct = mac._dopost('friend/approve_friend', postdata = param)
        time.sleep(1.414)
        # servant 自杀
        servant.end_contract()
        # master无须解除契约
        pass

    def ENTER__use_item(self, *args, **kwargs):
        mac = args[0]
        if not self.servant_pool_initialized:
            self.servant_pool = ServantPool(mac)
            self.servant_pool_initialized = True
            self.not_compatible = self.servant_pool.end_of_war
        if self.not_compatible:
            return
        self.excalibur(mac)
        return (mac, 0), kwargs # return pseudo id
