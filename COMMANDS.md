命令均以 “完整命令/缩写命令” 的形式给出，范例仅给出完整命令写法

###登陆

login/l

	login
	login username
	login username password
	

###设置卡组

set_card/sc

	set_card card_deck_key

card_deck_key为card_deck中已定义的项
	
###因子战

factor_battle/fcb

	factor_battle #自动选择碎片
	factor_battle lake:7 #选择湖7
	factor_battle lake:7 50 #选择湖7 且在BC<50时退出

	
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

###嗑绿茶

green_tea/gt

###自动卖卡

sell_card/slc

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
	reward_box 6 #只领取蛋卷奖励

###手动选择妖精战斗

fairy_select/fs

	fairy_select fairy.lv<60
	fairy_select fairy.lv<60 deck:min #选择lv60以下妖精，使用min卡组战斗

筛选条件语法与condition中的fairy_select相同

最后可跟deck:xxx表示强制使用该卡组战斗

###重新登录

relogin/rl

###问好

like/greet/gr

	like #使用默认问候语问好，若tactic中指定了问候语，则使用指定的问候语
	like 呵呵 #向所有好友问好 呵呵