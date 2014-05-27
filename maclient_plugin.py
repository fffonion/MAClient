#!/usr/bin/env python
# coding:utf-8
# maclient plugin loader and hooker
# Contributor:
#      fffonion        <fffonion@gmail.com>
import os, os.path as opath
import sys
import glob
import traceback
from cross_platform import *
# for plugin use
if PYTHON3:
    from io import StringIO
    import urllib.request as urllib2
else:
    from cStringIO import StringIO
    import urllib2
sys.path.append(opath.join(getPATH0, 'plugins'))
# os.chdir(opath.join(getPATH0(),'plugins'))
# sys.path[0]=os.path.abspath(opath.join(getPATH0,'plugins'))

PREF_ENTER = 'ENTER_'
PREF_EXIT = 'EXIT_'
EXTRAS_STACK_SIZE = 10
class plugins(object):
    def __init__(self, logger, mac_ver, show_tip = True):
        self.logger = logger
        # 是否显示插件tip
        self.show_tip = show_tip
        self.has_shown_tips = False
        self.mac_ver = mac_ver
        # 所有插件模块对象
        self.plugins = {}
        # 所有插件模块中的plugin实例
        self.plugins_instance = {}
        # 新增cli命令字典
        self.extra_cmd = {}
        # 从maclient实例映射的变量
        self.val_dict = {}
        #self.load_plugins()
        # self.scan_hooks()
        self.enable = True
        # 在被装饰函数内赋值，用于反向的传值
        self.extras = [{}]
        # 用于鉴别extras所属
        self.extras_last_token = ''
        # hook注册
        self.hook_reg = {}

    def scan_hooks(self):
        self.hook_reg.clear()
        ALL_ACTIONS = ['tasker', 'auto_check', 'check_strict_bc', 'set_card', 'red_tea', 'green_tea',
                    'explore', '_explore_floor', 'gacha', 'select_card_sell', 'fairy_battle_loop', 'fairy_select', '_fairy_battle',
                    'like', 'friends', 'reward_box', 'point_setting', 'factor_battle', 'invoke_autoset', '_exit', '_use_item']
        # scan plugin hooks
        _conflict = []
        _plugins_to_del = []
        self.extra_cmd.clear()
        for p in self.plugins:
            if self.show_tip and not self.has_shown_tips:
                try:
                    print('%s:%s' % (p, raw_du8(self.plugins[p].__tip__)))
                except AttributeError:
                    pass
            req_ver = self._get_module_meta(p, 'require_version', nowarning = True)
            if req_ver and req_ver > self.mac_ver:
                self.logger.warning('Plugin %s requires MAClient v%.2f or up.' % (p, req_ver))
                _plugins_to_del.append(p)
                continue
            # extra cmd
            ecmd = self._get_module_meta(p, 'extra_cmd')
            for e in ecmd:
                if e in self.extra_cmd or e in _conflict:
                    self.logger.warning('Command \"%s\" conflicted (in plugin %s).' % (e, p))
                    _conflict.append(e)
                    del(self.extra_cmd[e])
                else:
                    hdl = self._get_module_meta(p, ecmd[e])
                    if hdl:
                        self.extra_cmd[e] = hdl
            # function hook
            for act in ALL_ACTIONS:
                for method in [PREF_ENTER, PREF_EXIT]:  # enter, exit
                    key = '%s%s' % (method, act)
                    if key not in self.hook_reg:
                        self.hook_reg[key] = {}
                    if key in self._get_module_meta(p, 'hooks'):  # add to hook reg
                        # priority record
                        self.hook_reg[key][p] = self._get_module_meta(p, 'hooks')[key]
        self.has_shown_tips = True
        for p in _plugins_to_del:
            del(self.plugins[p])

    # def set_enable(self,lst):
    #     pass
    def set_maclient_val(self, val_dict):
        self.val_dict = val_dict

    def do_extra_cmd(self, cmd):
        ops = cmd.split(' ')
        if self.enable:
            try:
                ret = self.extra_cmd[ops[0]](self.val_dict)(' '.join(ops[1:]))
            except KeyboardInterrupt:
                pass
            except:
                errf = StringIO()
                traceback.print_exc(file = errf)
                self.logger.warning('执行命令"%s"时出现错误:\n%s' % 
                                    (cmd.rstrip(' '), errf.getvalue().replace('%','%%'))
                                   )
            else:
                return ret
        else:
            self.logger.warning('Plugins not enabled.')

    def set_disable(self, lst):
        for p in lst:
            if p and (p in self.plugins):
                del(self.plugins[p])

    def _get_module_meta(self, mod, key, nowarning = False):
        # module.xxx
        try:
           return getattr(self.plugins[mod], key)
        except AttributeError:
            if not nowarning:
                self.logger.warning('"%s" not found in module "%s"' % (key, mod))
            return []

    def _get_plugin_attr(self, mod, attr, nowarning = False):
        # module.plugin.xxx
        try:
           return getattr(self.plugins_instance[mod], attr)
        except AttributeError:
            if not nowarning:
                self.logger.warning('Get "%s" failed from "%s" ' % (attr, mod))
            return []

    def _do_hook(self, action, *args, **kwargs):
        if action in self.hook_reg:
            for plugin in sorted(self.hook_reg[action].items(), key = lambda d:d[1], reverse = True):  # high priority first
                f = self._get_plugin_attr(plugin[0], action)
                if f:
                    try:
                        ret = f(*args, **kwargs)
                    except KeyboardInterrupt:
                        pass
                    except:
                        errf = StringIO()
                        traceback.print_exc(file = errf)
                        self.logger.warning('挂钩%s时出现错误:\n%s' % 
                                            (action, errf.getvalue())
                                           )
                    else:
                        if ret:  # has mod on params
                            args, kwargs = ret
                            #args = args[1:]  # cut off caller instance variable
        return args, kwargs

    def load_plugins(self):
        import glob
        plugin_dir = opath.abspath(opath.join(getPATH0, 'plugins'))
        mods = glob.glob(opath.join(plugin_dir, '*.pyd')) + \
            glob.glob(opath.join(plugin_dir, '*.py')) + \
            glob.glob(opath.join(plugin_dir, '*.pyc')) + \
            glob.glob(opath.join(plugin_dir, '*.pyo'))
        # mods=[]
        modstr = ''
        last_mod = ''
        sys.path.insert(0, opath.join(getPATH0, 'plugins'))
        for m in mods:
            if ('.pyc' in m or '.pyo' in m) and m[:-1] in mods:#strip .pyc if .py exists
                continue
            m = opath.splitext(opath.split(m)[1])[0]
            if m.startswith('_'):
                continue
            if m not in self.plugins:
                # module object
                try:
                    self.plugins[m] = __import__(m)
                except:
                    self.logger.warning('%s is disabled due to an Error' % m)
                else:
                    # plugin instance
                    try:
                        self.plugins_instance[m] = self.plugins[m].plugin()
                        modstr = '%s,%s' % (modstr, m)
                    except AttributeError:
                        # no plugin() class
                        self.plugins_instance[m] = None
            last_mod = m
        sys.path.pop(0)
    # def _line_tracer(self):
    #     # originally from http://stackoverflow.com/questions/19227636/decorator-to-log-function-execution-line-by-line
    #     # it works almostly the same as module 'memory_profiler'
    #     # not working yet
    #     traced_func.add(func.func_code)
    #     def _wrapper(*args, **kwargs):  # need a wrap
    #         old_trace_function = sys.gettrace()
    #         sys.settrace(logging_tracer)
    #         try:
    #             result = func(*args, **kwargs)
    #         except:
    #             raise
    #         else:
    #             return result
    #         finally:
    #             sys.settrace(old_trace_function)
    #     return _wrapper
    
    def pop_extra(self, key):
        try:
            return self.extras[-1].pop(key)
        except IndexError:
            return None
        except KeyError:
            return None

    def pop_extra_current(self):
        #抛弃当前token未取完的所有extras
        self.extras.pop()

    def set_extras(self, token, key, val):
        #use a stack structure
        if token != self.extras_last_token:
            #上一次的可能还没取走，先保存起来
            self.extras.append({})
            self.extras_last_token = token
            if len(self.extras) > EXTRAS_STACK_SIZE:
                self.extras.pop(0)
        self.extras[-1][key] = val


    def func_hook(self, func):
        def do(*args, **kwargs):
            if self.enable:
                ret = self._do_hook('%s%s' % (PREF_ENTER, func.__name__), *args, **kwargs)
                args, kwargs = ret
                ret = func(*args, **kwargs)
                kwargs['pop_extras'] = self.pop_extra
                kwargs['_return'] = ret
                _pret = self._do_hook('%s%s' % (PREF_EXIT, func.__name__), *args, **kwargs)
                # if _pret:
                #    ret = _pret
                if not self.extras[-1] and len(self.extras) > 1:#已经取完了，且不是底
                    self.extras.pop()
                return ret
            else:
                return func(*args, **kwargs)  # passby
        return do

    def line_hook(self):
        pass

    # def __call__(self,func):
    #     return self.func_hook(func)

if __name__ == '__main__':
    import maclient_logging
    p = plugins(maclient_logging.Logging('logging'))
    # p.set_disable(['hehe'])
    # print p.plugins,p.hook_reg
    class a():
        @p.func_hook
        def explore(a, b, c, d = 1):
            print(1)
    aa = a()
    aa.explore(1, 2, 3, d = 3)
