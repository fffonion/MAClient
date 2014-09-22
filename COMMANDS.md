[For English Users](COMMANDS.en.md)

命令均以 “完整命令/缩写命令” 的形式给出，范例仅给出完整命令写法

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

###登陆

login/l

    login
    login username
    login username password
    

###设置卡组

set_card/sc

    set_card card_deck_key
    set_card auto_set(CONDITION)

保留的名称 no_change 不更改卡组，abort 直接跳出不战斗，letitgo 等妖精逃跑

card_deck_key为card_deck中已定义的项；当卡组名为auto_set时，此命令等效于auto_set CONDITION notest


###自动配卡

auto_set/as

    #所有参数均为可选参数
    #aim 目标，可选 max_dmg最大攻击输出(默认)，max_cp最大CP，defeat打败指定妖精
    #line 卡组排数，可选1(默认),2,3,4；若目标为DEFEAT，建议排数为1，时间复杂度太高了
    #fairy 如果目标是DEFEAT，则必须输入妖精信息，(默认为空)
    #   fairy:15,300000 15级的剩余血量30w的妖精
    #   fairy:15,300000,WAKE 15级的剩余血量30w的醒妖
    #delta 妖精血量误差(默认为1，即无误差)
    #bc 可选max 玩家最大BC，cur 当前剩余bc(默认)，或输入一个数值
    #notest 选出卡组后保存(无此参数时默认不保存)
    #>carddeck 配卡并保存到配置卡组的carddeck中
    #incl 包含某些卡片(默认为无) (现在还不能用)
    auto_set #选出一排当前剩余BC下最大攻击的卡组
    auto_set line:2 bc:max notest #选出两排不限BC的最大攻击卡组，并保存
    auto_set aim:defeat line:1 bc:cur fairy:30,263215 notest #选出一排能打死Lv30剩余hp263215的普妖的卡组，并保存
    auto_set aim:max_dmg line:1 bc:cur incl:124 #选出当前BC下一排最大攻击输出卡组，包括小狼女，不保存
    auto_set aim:max_cp line:1 bc:40 incl:124 > forty
    #选出cost40下一排最大CP卡组，包括小狼女，不保存，写入配置文件的forty卡组

###因子战

factor_battle/fcb

    factor_battle #自动选择碎片
    factor_battle lake:7 #选择湖7
    factor_battle lake:7 50 #选择湖7 且在BC<50时退出
    #可使用mf命令查询湖id与卡片的对应表（需启用map_factor_lakes插件）

###秘境探索

explore/e

    explore #根据condition自动选择秘境
    explore area.name=='學校教室'

筛选条件语法与condition中的auto_explore相同


###刷列表中的妖精

fairy_battle/fyb

    fairy_battle #根据system中确定的刷新次数
    fairy_battle 50 #刷新列表50次

###嗑红茶

red_tea/rt

    red_tea #红茶
    red_tea / #1/2红茶

###嗑绿茶

green_tea/gt

同红茶

###自动卖卡

sell_card/slc

    sell_card
    sell_card $.star in [1,2]

###自动合卡

buildup_card/buc

    buildup_card
    buildup_card $.star==7;$.star in [1,2] # buc 目标条件 狗粮条件

###设置账号类型

set_server/ss

    set_server cn
    set_server cn2
    set_server tw

###好友相关

friend/f

交互式菜单

###转蛋

gacha/g

    gacha 1 #绊转蛋
    gacha 2 #转蛋券转蛋
    gacha 4 #11连转蛋

###分配点数

point/p

交互式菜单

###礼物盒

reward_box/rb

    reward_box #领取全部奖励
    reward_box 12345 #领取全部奖励
    reward_box 1 #只领取卡片奖励
    reward_box 12 #只领取卡片和道具奖励
    reward_box 3 #只领取金币奖励
    reward_box 4 #只领取绊点奖励
    reward_box 5 #只领取蛋卷奖励
    reward_box 5> #只领取蛋卷奖励，且不打印奖励详情
    reward_box [^級極]切 #领取所有切尔莉，不包括超级和究极

支持正则表达式

###手动选择妖精战斗

fairy_select/fs

    fairy_select fairy.lv<60
    fairy_select fairy.lv<60 deck:min #选择lv60以下妖精，使用min卡组战斗

筛选条件语法与condition中的fairy_select相同

最后可跟`deck:xxx`表示强制使用该卡组战斗；可以使用自动配卡，即`deck:auto_set(CONDITION)``

###重新登录

relogin/rl

###问好

like/greet/gr

    like #使用默认问候语问好，若tactic中指定了问候语，则使用指定的问候语
    like 呵呵 #向所有好友问好 呵呵