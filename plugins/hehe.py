from _prototype import plugin_prototype
#start meta
__plugin_name__='sample plugin'
__author='fffonion'
__version__=0.1
#hooks={'ENTER/EXIT_ACTION':PRIORITY}
#eg:
#hook on explore start with priority 1 (the bigger the higher):
#'ENTER_explore':1
hooks={'ENTER__fairy_battle':1,'EXIT__fairy_battle':1,'ENTER_explore':1}
#extra cmd hook
extra_cmd={}
#end meta
class plugin(plugin_prototype):
    def __init__(self):
        self.__name__=__plugin_name__

    def ENTER_explore(self,*args, **kwargs):
        print 'explore!'
        print args
        #must return input vals. no matter you've changed it or not
        return args,kwargs

    def EXIT__fairy_battle(self,*args, **kwargs):
        print 'fairy_battle done!'
        return args,kwargs

    def ENTER__fairy_battle(self,*args, **kwargs):
        print 'fairy_battle!'
        return args,kwargs