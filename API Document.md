VERSION 1.0

本文档介绍使用python和其他后台的web应用与maClient的通信方式


##Python后台应用
典型的使用方法如下：
```Python
import maclient
mac = maclient.maClient()
xml=mac.login(uname='xxxx',pwd='xxxx')
mac.initplayer(xml)
```
初始化完成之后可以使用tasker来执行任务
```Python
mac.tasker('set_card factor|factor_battle')
```
有关tasker的使用方法请参阅[readme](https://github.com/fffonion/maClient/blob/master/README.md)


##其他应用
你需要继承并扩展maclient_remote类
除了下面提到的属性和方法，其他内容是中间变量或被类自动管理，无需修改

###属性
name 名称
home 应用的home url
status 启动状态
iprofile 保存了玩家信息
task 下一步maclient要执行的命令

###方法

####__init__
初始化时有四个须传入的参数：name='',home='',statusloop=30,profileloop=180

分别为名称(随便取)，应用的home url，查询工作状态的周期，上传玩家信息的周期

也可以直接在__init__中赋值，这样就不用在新建实例的时候传入

每次工作状态的检查都只发生在maclient进行网络操作时，这表示工作状态的改变不一定会在设定的statusloop时间内反映在maclient中

####login
当maclient的set_remote被调用后自动被执行，须返回一个元组，内容为(是否登录成功，提示信息)

比如，可以在这个方法中得到一个cookie以供后续操作。无需显式地处理cookie，maclient_remote自动使用得到的cookie

需要继承maclient_remote的login方法
        
####queryloop
查询工作状态的代码，通过应用返回值来重新设定self.status，可选有STARTED,STOPPED

还可以设定self.task字符串，以通知maclient下一步要执行的命令

####upload_profile
上传玩家信息的代码，玩家信息会被实时更新到self.iprofile字典中，目前可用的内容有ap_current, ap_max, bc_current, bc_max, gold

####fckfairy
当玩家进行一次妖精战时，本方法被调用一次，传入一个名为fairy的object_dict，可得到fairy.name, fairy.lv, fairy.hp等属性值

当需要网络操作时，可以使用方法self.do(uri='',param='',method='GET')，传入uri，上传的内容(POST或GET中分别表示post data和query string)，方法（'POST','GET'），返回值为回调内容
已支持cookie

在maclient_plugin_test中可以是这样的：
```Python
import maclient_remote
class test(maclient_remote.maRemote):
    def __init__(self,uname='',pwd=''):
        maRemote.__init__(self,name='test',home='http://abcd-maclient.rhcloud.com/',statusloop=30,profileloop=180)
        self.uname=uname
        self.pwd=hashlib.md5('123%s1232'%pwd).hexdigest()
        #return self.login()

    def login(self):
        res=self.do(uri='login.php',param=urllib.urlencode({'u':self.uname,'p':self.pwd},method='POST'))
        if res=='0':
            maclient_remote.maRemote.login(self)
            return True,'login successfully'
        return False,'login failed'

    def queryloop(self):
        res=self.do(uri='query.php'))
        #print res
        if res=='start':
            self._set_status(self.STARTED)
        elif res=='stop':
            self._set_status(self.STOPPED)

    def upload_profile(self):
        self.do(uri='profile.php',param=urllib.urlencode(
        {'AP':self.iprofile['ap_current'],
        'BC':self.iprofile['bc_current']},
        method='POST'))

    def fckfairy(self,fairy):
        self.do(uri='fairy.php'))
```      
在完成一个扩展的maclient_remote后（假设为maclient_plugin_test），你需要使用maclient（假设存在一个实例mac1）的set_remote方法绑定这个扩展
```Python
import maclient_plugin_test as test
mpt=test.test(uname='test',pwd='test')
mac1.set_remote(mpt)
```