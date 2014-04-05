# coding:utf-8
from _prototype import plugin_prototype
from cross_platform import *

# start meta
__plugin_name__ = '重置连接池工具'
__author = 'fffonion'
__version__ = 0.2
hooks = {}
extra_cmd = {'rs':'reload_socket', 'reload_socket':'reload_socket'}
# end meta
# 
def reload_socket(plugin_vals):
    def do(args):
        for s in plugin_vals['poster'].ht.connections:
            plugin_vals['poster'].ht.connections[s].close()
        print(du8('已释放%d个连接' % len(plugin_vals['poster'].ht.connections)))
        plugin_vals['poster'].ht.connections = {}
    return do
