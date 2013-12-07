#coding:utf-8
from _prototype import plugin_prototype
#start meta
__plugin_name__='自动探索限时秘境，嗑绿'
__author='fffonion'
__version__=0.1
__tip__='请确保 【限时】神界战争通道 已被优先选择'
import datetime
hooks={'ENTER__explore_floor':1,'EXIT_explore':1}
#extra cmd hook
extra_cmd={}
#end meta
class plugin(plugin_prototype):
    def __init__(self):
        self.__name__=__plugin_name__
        self.has_enter_limit_area=False
        self.mac_instance=None

    def ENTER__explore_floor(self,*args, **kwargs):
        #args self,area,eval
        self.logger=args[0].poster.logger
        if '战争通道' in args[1].name:
            if args[1].prog_area=='100':
                self.logger.info('plugin:限时秘境已探索完成www')
            else:
                self.logger.info('plugin:限时秘境已开启于:%d点'%datetime.datetime.now().hour)
                self.has_enter_limit_area=True
                self.mac_instance=args[0]

    def EXIT_explore(self,*args, **kwargs):
        if self.has_enter_limit_area:
            if self.mac_instance.player.ap['current']<5:
                self.logger.info('plugin:AP用完了吗(剩余%d)？来一瓶吧'%self.mac_instance.player.ap['current'])
                if not self.mac_instance.green_tea():#优先使用自动配额
                    self.mac_instance._use_item('1')
            self.has_enter_limit_area=False