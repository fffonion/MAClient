from _prototype import plugin_prototype
#start meta
__name__='sample plugin'
__author='fffonion'
#hooks={'ENTER/EXIT_ACTION':PRIORITY}
#eg:
#hook on explore start with priority 1 (the bigger the higher):
#'ENTER_explore':1
hooks={'ENTER__fairy_battle':1,'EXIT__fairy_battle':1,'ENTER_explore':1}
#end meta
class plugin(plugin_prototype):

    #must add classmethod decorator
    @classmethod
    def ENTER_explore(self,*args, **kwargs):
        print 'explore!'
        #must return input vals. no matter you've changed it or not
        return args,kwargs

    @classmethod
    def EXIT__fairy_battle(self,*args, **kwargs):
        print 'fairy_battle done!'
        return args,kwargs

    @classmethod
    def ENTER__fairy_battle(self,*args, **kwargs):
        print 'fairy_battle!'
        return args,kwargs