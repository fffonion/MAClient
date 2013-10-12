#!/usr/bin/env python
# coding:utf-8
# maclient plugin loader and hooker
# Contributor:
#      fffonion        <fffonion@gmail.com>
import os,os.path as opath
import sys
import glob
getPATH0=(opath.split(sys.argv[0])[1].find('py') != -1 or sys.platform=='cli') \
         and sys.path[0].decode(sys.getfilesystemencoding()) \
         or sys.path[1].decode(sys.getfilesystemencoding())#pyinstaller build
sys.path.append(opath.join(getPATH0,'plugins'))
#os.chdir(opath.join(getPATH0(),'plugins'))
#sys.path[0]=os.path.abspath(opath.join(getPATH0,'plugins'))
        
PREF_ENTER='ENTER_'
PREF_EXIT='EXIT_'
class plugins():
    def __init__(self,logger):
        self.traced_func = set()
        self.plugins=[]
        self.load_plugins()
        self.scan_hooks()
        self.logger=logger
        self.enable=True

    def scan_hooks(self):
        self.hook_reg={}
        ALL_ACTIONS=['tasker','auto_check','check_strict_bc','set_card','red_tea','green_tea',
                    'explore','_explore_floor','gacha','select_card_sell','fairy_battle_loop','fairy_select','_fairy_battle',
                    'like','friends','reward_box','point_setting','factor_battle']
        #scan plugin hooks
        for act in ALL_ACTIONS:
            for p in self.plugins:
                for method in [PREF_ENTER,PREF_EXIT]:#enter, exit
                    key='%s%s'%(method,act)
                    if key not in self.hook_reg:
                        self.hook_reg[key]={}
                    if key in self._get_plugin_meta(p,'hooks'):#add to hook reg
                        self.hook_reg[key][p]=self._get_plugin_meta(p,'hooks')[key]      
    # def set_enable(self,lst):
    #     pass

    def set_disable(self,lst):
        for p in lst:
            if p:
                del(self.plugins[self.plugins.index(p)])
        self.scan_hooks()

    def _get_plugin_meta(self,mod,key):
        try:
            return getattr(globals()[mod],key)
        except AttributeError:
            self.logger.warning('No meta found for module "%s"'%mod)
            return []

    def _get_plugin_attr(self,mod,attr):
        try:
            return getattr(globals()[mod].plugin(),attr)
        except AttributeError:
            self.logger.warning('Get "%s" failed from "%s" '%(attr,mod))
            return []

    def _do_hook(self,action,*args,**kwargs):
        if action in self.hook_reg:
            for plugin in sorted(self.hook_reg[action].iteritems(), key=lambda d:d[1], reverse = True):#high priority first
                f=self._get_plugin_attr(plugin[0],action)
                if f!=[]:
                    args,kwargs=f(*args, **kwargs)
        return args,kwargs
    
    def load_plugins(self):
        import glob
        plugin_dir=opath.abspath(opath.join(getPATH0,'plugins'))
        mods=glob.glob(opath.join(plugin_dir,'*.py'))+\
            glob.glob(opath.join(plugin_dir,'*.pyc'))+\
            glob.glob(opath.join(plugin_dir,'*.pyo'))+\
            glob.glob(opath.join(plugin_dir,'*.pyd'))
        for m in mods:
            m=opath.splitext(opath.split(m)[1])[0]
            if m=='_prototype':
                continue
            if m not in self.plugins:
                globals()[m]=__import__(m)
                self.plugins.append(m)

    def _line_tracer(self):
        #originally from http://stackoverflow.com/questions/19227636/decorator-to-log-function-execution-line-by-line
        #it works almostly the same as module 'memory_profiler'
        #not working yet
        traced_func.add(func.func_code)
        def _wrapper(*args, **kwargs):#need a wrap
            old_trace_function = sys.gettrace()
            sys.settrace(logging_tracer)
            try:
                result = func(*args, **kwargs)
            except:
                raise
            else:
                return result
            finally:
                sys.settrace(old_trace_function)
        return _wrapper

    def func_hook(self,func):
        def do(*args, **kwargs):
            if self.enable:
                args,kwargs=self._do_hook('%s%s'%(PREF_ENTER,func.__name__),*args, **kwargs)
                ret=func(*args, **kwargs)
                self._do_hook('%s%s'%(PREF_EXIT,func.__name__))
                return ret
            else:
                return func(*args, **kwargs)#passby
        return do

    def line_hook(self):
        pass

    # def __call__(self,func):
    #     return self.func_hook(func)

if __name__=='__main__':
    import maclient_logging
    p=plugins(maclient_logging.Logging('logging'))
    p.set_disable(['hehe'])
    #print p.plugins,p.hook_reg
    @p.func_hook
    def explore(a,b,c,d=1):
        print 1
    explore(1,2,3,d=3)
    