maClient Plugin Document
================
本文档给出maclient插件制作的标准和一些参考

*   [概述](#概述)
*   [HOOK插件](#hook插件)
    *   [示例](#示例)
    *   [结构](#结构)
    *   [事件名称](#可用事件名称)
    *   [应用](#应用)
*   [EXTRA_CMD插件](#extra_cmd插件)
    *   [示例](#示例-1)
    *   [结构](#结构-1)
    *   [有用的变量](#有用的变量)
    *   [应用](#应用-1)

##概述

maclient1.50版本开始支持插件，通过在配置项中的“启用插件”功能(enable_plguins)和“禁用单个插件”选项(disabled)来控制插件的启用与否。

插件为py脚本，放置在plugins目录下，由maclient_plugin在运行时载入；其中下划线开头的脚本和子目录中的脚本 __不会__ 被载入；同名脚本的优先级为pyd>py>pyc=pyo

插件分为两类，一类在指定的事件发生前和发生后作出响应(下称[hook插件](#HOOK插件))，另一类给命令行界面(cli)增加新命令(下称[extra_cmd插件](#EXTRA_CMD插件))；__两种类型可以存在于同一个文件内__。

##HOOK插件

###示例

[example_hook](plugins/_example_hook.py) [bgm](plugins/bgm.py)

###结构

下面以example_hook为例；在这个例子中，在开始攻击妖精 、 结束攻击妖精 和 进入探索 三个事件发生时分别在屏幕上打印一句话

开头需从_prototype导入plugin_prototype父类；然后定义插件名称，作者，版本：
```Python
from _prototype import plugin_prototype
__plugin_name__='sample plugin'
__author='fffonion'
__version__=0.1
```

定义事件钩子，即ENTER/EXIT _ EVENT_NAME：
```Python
hooks={'ENTER__fairy_battle':1,'EXIT__fairy_battle':1,'ENTER_explore':1}
```

###可用事件名称

    tasker 任务调度器
    auto_check 自动检查卡片、绊点是否已满 
    check_strict_bc 检查是否触发严格BC
    set_card 设置卡组
    red_tea 嗑红茶
    green_tea 嗑绿茶
    explore 探索：选择地区
    _explore_floor 探索：走路
    gacha 转蛋
    select_card_sell 自动卖卡
    fairy_battle_loop 刷新妖精列表循环
    fairy_select 选择妖精
    _fairy_battle 攻击妖精
    like 问好
    friends 好友相关
    reward_box 领取礼物盒
    point_setting 分配点数
    factor_battle 因子战
    invoke_autoset 自动配卡

冒号后的数值表示钩子的优先级，越大则越先被调用

如例子中定义了在 开始攻击妖精 、 结束攻击妖精 和 进入探索 三个事件的钩子，优先级为1（最低）

*如果不需要extra_cmd，此处留空字典*
```Python
extra_cmd={}
```

类实例
```Python
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
```
类名称必须为plugin，且继承plugin_prototype父类

对每个事件钩子，必须有一个同名的类方法，args 和 kwargs 中被传入了这个事件被调用时传入的参数。

可以使用self.tuple_assign（继承自父类）修改args中参数内容，如self.tuple_assign(args, 0, '123')#将args第一个参数改为123

*如果没有return语句或return后无参数，则默认为不修改参数*

*类运行时会先生成一个实例，因此你可以保存一些状态信息等*

关于参数的具体内容可以 __参阅[maclient.py](maclient.py)__

###应用

示例中的[bgm](plugins/bgm.py)插件，仅额外使用了一个栈结构就实现了bgm的切换


##EXTRA_CMD插件

###示例

[web_helper](plugins/web_helper.py) [query_tool](plugins/query_tool.py)

###结构

meta部分与hook插件相同，区别仅在于extra_cmd字典中需填入扩展命令的值和内容

字典的key表示扩展命令，value表示要执行的函数：
```Python
extra_cmd={'web':'start_webproxy','w':'start_webproxy'}
```

采用函数式结构，返回函数的名称随便取，不一定是do：
```Python
def start_webproxy(plugin_vals):
    def do(*args):
        .....
    return do
```

在plugin_vals中传入了maclient在运行中的 __所有实例变量__

###有用的变量

    plugin_vals['poster'] maclient_network中的poster实例，可用于通信，返回已解密的内容
    plugin_vals['player'] 玩家实例
    ├─.cards 卡片数据
    │  └ .db 卡片数据库 {1:['第一型兰斯洛特','5','19'],……}
    │  └ .cards 玩家所拥有的卡片 ，列表，元素为object_dict类型
    │  └ .sid(xxx) 按serial_id找卡片
    │  └ .mid(xxx) 按master_card_id找卡片，返回列表
    ├─.item 卡片数据
    │  └ .name 道具数据库 {'1':'AP回复药',……}
    │  └ .count 道具数量，如{'1':123}表示1号道具有123个
    ├─.ap / bc
    │  └ ['cur'] 当前值
    │  └ ['max'] 最大值
    ├─.friendship_point / gold
    plugin_vals['loc'] 服务器名称
    plugin_vals['cookie'] 小饼干
    plugin_vals['poster'].logger 输出日志用

其他变量请 __参阅[maclient.py](maclient.py)__，所有以self.开头的变量均可使用

###应用

[web_helper](plugins/web_helper.py)借助小饼干和一个代理，实现了在电脑浏览器上查看活动信息等
