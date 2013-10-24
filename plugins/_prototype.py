#import dbm
class plugin_prototype():
    def __init__(self):
        self.hooks={}
        
    @classmethod
    def register_action(self,action,priority=0):
        self.hooks[action]=priority

    def tuple_assign(self,ori_tuple,index,val):
        new=list(ori_tuple)
        new[int(index)]=val
        return tuple(new)

    def setval(self,key,val):
        pass#print self.__name__

    # @classmethod
    # def __call__(self,func):
    #     raise NotImplementedError("%s is called, but not implemented."%func)