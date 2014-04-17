MAClient是一个可以用来装B的百万亚瑟王客户端。支持台服、国服全区、韩服、日服和东南亚(新加坡)服。

##文档

[更新历史](https://github.com/fffonion/MAClient/wiki/HISTORY)

[插件制作文档](PLUGIN_DOCUMENT.md)

##运行

###Windows

Windows用户可以从[这里](http://pan.baidu.com/s/19qI4m)获得二进制文件，或者从[release](https://github.com/fffonion/MAClient/releases)下载

**注意1**：路径不能包含中文，这是pyinstaller的缺陷

**注意2**：运行韩服和日服时，推荐使用[MAClientGUI](http://mac.yooooo.us/MAClientGUI.zip)中的**终端模拟器**

###网页版

MAClient可以在支持websocket的浏览器上运行![chaojibang](http://ww1.sinaimg.cn/bmiddle/436919cbjw1ebx3ktnokkg200m00k741.gif)[炒鸡棒在线版](http://ma.mengsky.net/)

###Android

参见 [在Android设备上运行MAClient](https://github.com/fffonion/MAClient/wiki/%E5%9C%A8Android%E6%89%8B%E6%9C%BA%E4%B8%8A%E8%BF%90%E8%A1%8CMAClient)

###Linux/OS X/wwww
需要下载修改的[httplib2库](https://github.com/fffonion/httplib2-plus)，自行编译PyCrypto库

MAClient可以在python2.x和3.x上运行
```shell
git clone --recursive https://github.com/fffonion/MAClient.git
cd httplib2
python setup.py install
```
子模块为针对py2x的httplib2；对py3x，你需要下载[py3x适用的httplib2](https://github.com/fffonion/httplib2-plus/tree/python3)
```shell
python MAClient_cli.py
python MAClient_cli.py [config file]
python MAClient_cli.py [config file] [task]/[commands]
```
将maclient_smart编译成C模块可以提高自动配卡速度
```shell
python build_cython_ext.py build_ext --inplace
```


##配置文件说明

参考config_sample.ini，以及[**这里**](http://pan.baidu.com/s/19qI4m#dir/path=%2FApp%2FMAClient%2F%E7%A4%BA%E4%BE%8B%E9%85%8D%E7%BD%AE)有一些参考配置

或者使用图形化配置工具MAClientGUI，它可以从[这里下载](http://mac.yooooo.us/MAClientGUI.zip)，相关源代码可以从[这里获得](https://github.com/fffonion/MAClient/tree/gui)

***

###account_?

?可选`cn`,`cn2`,`cn3`,`tw`,`kr`,`jp`,`sg` 分别对应国服1区，国服2区，国服3区，台服，韩服，日服，东南亚服

session不用管它


###carddeck

####卡组列表

值可选卡片id或者卡片序列号

如：

    min=124 #选出小狼女
    factor=93714777,54276719 

请保证存在`min`项且值为舔刀卡组，以保证省流模式工作正常

如果你卡片中存在小狼女，那么请不要大意地忽略这句话吧ww
	
###system

系统设置

####server

选服，可选`cn`,`cn2`,`cn3`,`tw`,`kr`,`jp`

####loglevel

屏幕输出日志级别，可选0-6，嫌烦就调大点

####taskname

表示需要程序执行的任务名称（tasker中），|分割

####tasker_times

表示要执行任务的次数，0为无限

####try_factor_time

是刷因子战列表的次数，0为无限

####factor_sleep

刷列表的间隔(秒)

####explore_sleep

刷秘境的间隔(秒)

####fairy_battle_times

刷妖精列表次数

####fairy_battle_sleep

刷妖精列表间隔(分)，按时间设置，比如0-5点每5分刷新一次，5-10点每2分刷新一次： 0,5,5|5,10,2，若不在范围内，默认1.5分

####fairy_battle_times

刷妖精列表间隔因数，用于将间隔时间全部缩放一个倍数

####delay

设置POST延迟，默认关闭，设为0时会提示WARNING

####allow_long_sleep

是否允许长睡眠，在某些操作系统上后台进程长时间睡眠会被kill，可以禁用此项

####reconnect_gap

断线重连策略，可选(1)数字，在指定分钟后重连, (2)HH:MM，在指定时刻重连

###tactic

策略

####auto_explore

是否自动选择秘境(按照`explore_area`和`explore_floor`规则)，是为1

####auto_green_tea,auto_red_tea

设置嗑药次数，当前任务已是自动任务时，若此项设为0，则会在AP/BC不足时直接退出

####auto_red_tea_level

自动嗑药条件1.满足条件的觉醒自动嗑红，2.满足条件的普妖嗑红，0.不嗑药(BC不足就跳过）

####auto_choose_red_tea

自动选择红茶类型，如果半红可以满足战斗cost则嗑半红，否则嗑全红

####strict_bc

严格BC模式, 打开时，当前BC低于卡组cost时认为BC不足(只影响妖精战)

####auto_sell_card

到≥200张了是否自动卖卡，按照`select_card_to_sell`规则

####auto_fp_gacha

绊点到9900了是否自动转蛋

####fp_gacha_bulk

是否批量绊转蛋（一次10张

####auto_build

是否自动合成相同卡片，默认为1，只影响探索和转蛋中的一星/二星卡

####auto_fairy_rewards

自动领取妖精奖励

####sell_card_warning

卖卡提醒，可设置2:全提醒 ，1:R+提醒，0:不提醒

####del_friend_day

删除几天以上没上线的好友

####fairy_final_kill_hp

若打完妖精后血量低于设定值则立即再打一次，默认为20000


###tasker

任务切换；Moore机

可以建立多个任务表达式，每个表达式用|分割，单个任务用空格分割命令和参数，

可选：

登陆 `login`/`l`, 设置卡组 `set_card`/`sc`,因子战 `factor_battle`/`fcb`,秘境探索 `explore`/`e`,刷列表中的妖精 `fairy_battle`/`fyb`,嗑药 `red_tea`/`rt` `green_tea`/`gt`,自动卖卡 `sell_card`/`slc`,设置账号类型 `set_server`/`ss`,好友相关 `friend`/`f`,转蛋`gacha`/`g`,分配点数`point`/`p`,礼物盒`rewardbox`/`rb`(可后跟参数 12345 分别表示 卡片 道具 金 绊点 蛋卷),手动选择妖精战斗`fairy_select`/`fs`,重新登录`relogin`/`rl`,问好`like`/`greet`/`gr`

以t:开头可执行任务

其中`explore`，`sell_card`后可选参数以指定条件，否则按照condition中的条件执行;`factor_battle`可选参数 最低BC，默认为0；`fairy_battle`可选参数 循环次数，默认按照config中所指定的次数

如：

    login heheh 123456 #登陆 
    set_server cn|set_card factor|factor_battle #设置国服，设置因子战卡组，然后因子战
    ss cn|sc factor|fcb #同上
    explore '明鏡月和島' in area.name #探索秘境名称包含'明鏡月和島' 
	fcb l:1 70 或 fcb lake:1 70#因子战选择第一因子，下限BC70，因子默认为随机选择，BC下限默认为0

各命令及参数的详细介绍见[COMMANDS文档](COMMANDS.md)

###condition
指定满足什么条件时做什么事

全局可用的量：

    HH 当前(24小时制的)小时
    MM 当前分钟
    BC 剩余bc
    BC% 剩余bc百分比，小数
    AP 剩余ap
    AP% 剩余ap百分比，小数
    SUPER 累积的super值
    GOLD 金币
    FP 友情点数
    FAIRY_ALIVE 自己发现的妖精是否存活
    GUILD_ALIVE 公会的妖精是否存活

PS:你必须进入一次妖精列表（使用`fairy_battle`/`fyb`或`fairy_select`/`fs`）才能刷新FAIRY_ALIVE和GUILD_ALIVE的值

PPS:当表达式中的主语可以被唯一确定时（变量只有一个），可以用'$'代替之

如`explore_area`表达式中，`$.IS_EVENT`和`area.IS_EVENT`是等价的

####factor
因子战需满足的表达式

变量：

`star`，`cid`，分别对应头像的星数和卡片id, 其他变量严重影响游戏公平性, 不作公开

eg:

    start ==1 or star ==2或star in [1,2] #卡片为一星或两星
    cid in [124,8,256] #队长卡片id为124,8或256：

####explore_area
选择秘境满足的表达式，支持多个条件，留空表示随机

变量：`area`

属性：

活动秘境 `IS_EVENT`, ~~每日秘境 `IS_DAILY_EVENT`~~, 公会秘境 `IS_GUILD`, 未刷完 `NOT_FINNISHED`, 秘境名称 `name`

eg.：

    area.IS_EVENT and area.NOT_FINNISHED　#想进入一个没完成的活动秘境
    area.name == ' 學校四樓教室' #进入 学校四楼教室
	area.NOT_FINNISHED | area.IS_EVENT #进入没完成的秘境；如果不存在没完成的秘境，则选择一个活动秘境
	area.NOT_FINNISHED | 进入没完成的秘境；如果不存在没完成的秘境，则选择任一秘境

####explore_floor
选择地区满足的表达式，支持多个条件，留空表示随机

变量：`floor`

属性：

未刷完 `NOT_FINNISHED`, AP消耗 `cost`

eg.：

    floor.cost<6 and floor.NOT_FINNISHED #进没完成的且cost小于6的地区：
	floor.cost<3 | #进cost<3的地区；如果没有则随机选择一个地区

####fairy_select
妖精列表里的什么妖精要打

变量：`fairy`

属性：

是我开的 `IS_MINE`,剩余时间 `LIMIT`(单位为秒),没打过 `NOT_BATTLED`,等级 `lv`,是否觉醒 `IS_WAKE`,是否稀有妖精 `IS_WAKE_RARE`,是否公会妖精 `IS_GUILD`

eg.：

    not fairy.IS_MINE and fairy.LIMIT<600 and fairy.NOT_BATTLED #打不是我发现的，剩余时间为10分钟的，还没舔过的妖精

####fairy_select_carddeck
遇到什么样的妖精时选择什么样的卡组

变量：`fairy`

属性：

`lv`,`hp`,`name`,`IS_MINE`, 剩余时间 `TIME_LIMIT`(单位为秒), 是否觉醒 `IS_WAKE`, 是否稀有妖精 `IS_WAKE_RARE`,是否公会妖精 `IS_GUILD`

只能使用and or表达式 或if else表达式，可嵌套；卡组名称需加引号，需在carddeck中给出；可以使用'no_change'表示不更改卡组

eg.：

    fairy.hp>200000 and 'tiandao' or 'full' 也可写作 'tiandao' if fairy.hp>200000 else 'full'　#遇到hp>200000的妖精用卡组tiandao，否则用full
    'no_change' #不改变

####select_card_to_sell
自动卖卡卖哪些

变量：`card`

属性：

`star`,`lv`,序列号 `sid`,卡片编号 `cid`，贩卖价格`price`, 是否闪卡`holo`

eg：

    card.star in [1,2] and card.lv<5 and card.cid != 124 and not card.holo #1星2星 lv5一下的卡且不是小狼女且不是闪卡:

注：
已自动排除所有小切切；如果不慎选入R及以上的卡，会出现提示确认