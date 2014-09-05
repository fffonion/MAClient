MAClient is a full-featured client for Million Arthur. Currently support Mobimon server(tw), SNDA server(cn), Actoz server(kr), Japan server(jp), and Cherry server(sg).

##Documents

For [History](https://github.com/fffonion/MAClient/wiki/HISTORY)

[Plugin document](PLUGIN_DOCUMENT.en.md)

##Running

###Windows

Windows users can obtain pre-bundled binary files from [here](http://pan.baidu.com/s/19qI4m#dir/path=%2FApp%2FMAClient) or from [release](https://github.com/fffonion/MAClient/releases)

**Tip1**：Make sure path only contais ASCII characters, this is a bug from pyinstaller.

**Tip2**：If you're using kr server or jp server on Chinese or English version of Windows, try use **NiceTerm**(Terminal Emulator) in [MAClientGUI](https://github.com/fffonion/MAClient/tree/gui)

###Web version

MAClient runs on a browser that is [websocket ready](http://caniuse.com/#search=websocket) ![chaojibang](http://ww1.sinaimg.cn/bmiddle/436919cbjw1ebx3ktnokkg200m00k741.gif)[Running demo](http://ma.mengsky.net/)

###Android

Refer to [Run MAClient on Android Devices](https://github.com/fffonion/MAClient/wiki/%E5%9C%A8Android%E6%89%8B%E6%9C%BA%E4%B8%8A%E8%BF%90%E8%A1%8CMAClient#en)

###Linux/OS X/what else
Install httplib2 from [here](https://github.com/fffonion/httplib2-plus) or from PIP，and PyCrypto. You need **python-devel** and a working toolchain to build PyCrypto from source code.
```
sudo pip install httplib2 Crypto
```

####KR Server dependency library
Refer to [release](https://github.com/fffonion/MAClient/releases/tag/kr-crypt-ext) for a download. This library is not opensource at thie time.

MAClient runs on python2.x (Recommand) and 3.x
```shell
git clone --recursive https://github.com/fffonion/MAClient.git
cd httplib2
python setup.py install
```
The httplib2 submodule is for py2x; for py3x, download [here](https://github.com/fffonion/httplib2-plus/tree/python3)
```shell
python MAClient_cli.py
python MAClient_cli.py [config file]
python MAClient_cli.py [config file] [task]/[commands]
```
Compile `maclient_smart` to C extension to get faster auto_set speed. Before running the following command, you need to install Cython, python-devel, and a working toolchain.
```shell
python build_cython_ext.py build_ext --inplace
```



##Configuration

Refer to config_sample.ini，or [**here**](http://pan.baidu.com/s/19qI4m#dir/path=%2FApp%2FMAClient%2F%E7%A4%BA%E4%BE%8B%E9%85%8D%E7%BD%AE)for some configured files.

You can also use MAClientGUI, a handy configrating tool. [Download](http://pan.baidu.com/s/19qI4m#dir/path=%2FApp%2FMAClient) [Source code](https://github.com/fffonion/MAClient/tree/gui)

***

###account_?

? can be either `cn`,`cn2`,`cn3`,`tw`,`kr`,`jp`,`sg`, which means:
Mobimon server(tw), SNDA server(cn), Actoz server(kr), Japan server(jp), and Cherry server(sg).

####username, password
you know

####session, user_id
ignore


###carddeck

####carddeck list

The value can be either card id or serial id. Serial id differs from user to user.

eg:

    min=124 #Second - Bisclavret
    factor=93714777,54276719

Please make sure `min` item is for **lick fairy**, so that `save_traffic` mode works well.

**lick fairy** means only touch the fairy to get minimun damage and reward.
    
###system

System Configurations

####server

server code `cn`,`cn2`,`cn3`,`tw`,`kr`,`jp`,`sg`

####loglevel

int from 0-6, 0 for debug output

####taskname

the task name from keys in `tasker` section, use `|` to split multiple tasks

####tasker_times

the loop time when doing a task, 0 = infinite

####try_factor_time

the loop time when refreshing factor battle list, 0 = infinite

####factor_sleep

the sleep interval when refreshing factor battle list

####explore_sleep

the sleep interval when exploring

####fairy_battle_times

the loop time when refreshing fairy list, 0 = infinite

####fairy_battle_sleep

the sleep interval of refreshing fairy list. eg:`0,5,3|5,10,2` means sleep 3 min when it's between 0~5 o'clock, and 2 min between 5~10 o'clock. Otherwise, sleep 1.5 min by default

####fairy_battle_times

the factor of sleep interval of refreshing fairy list. `factor * the_sleep_time_in_fairy_battle_sleep = real_sleep_time`

####delay

delay between two POST request, will show WARNING if set to 0

####allow_long_sleep

whether long time sleep is allowed. on some OS, long time sleeping in the background may call the process to be killed.

####reconnect_gap

when to reconnect if the server returns cookie expired. two format is supported

(1)int, reconnect in INT minutes

(2)HH:MM, reconnect at system time HH:MM

###tactic

the tactics

####auto_explore

whether explore area automatically (following rules in `explore_area`和`explore_floor`), 1 by default

####auto_green_tea, auto_red_tea

the limit of auto using potion. set to 0 to disable auto using potion

####auto_red_tea_level

use red potion in what situation 1.all wake fairies，2.all normal fairies，0.disabled

####auto_choose_red_tea

whether choose red potion type automatically. if a half potion meets battle cost, then use half potion

####strict_bc

if enabled, a **no bc break** will be raised if BC left < battled cost, this will lead to auto using potion or aborting battle(only fairy battled is affected)

####auto_sell_card

whether sell card automatically when card package is full, following `select_card_to_sell`

####auto_fp_gacha

whether run friendship gacha automatically when friendship point is 99% of the limit.

####fp_gacha_bulk

whether run bulk friendship gacha (10 cards a time)

####auto_build

whether auto compound cards in explore and friendship gacha

####auto_fairy_rewards

automatically get fairy rewards

####sell_card_warning

value 2:warns all ，1:warns for R+，0:no warning

####del_friend_day

delete friends that is not login for ? days

####fairy_final_kill_hp

beat the fairy again if the fairy's hp is lower than ?

20000 by default


###tasker

setup tasks; it's a Moore state machine

You can specify multiple action expressions with `|` as seperator; seperate command and args using SPACE in single expression

Command list:

login `login`/`l`, set carddeck `set_card`/`sc`, factor battle `factor_battle`/`fcb`, explore dungeon `explore`/`e`, refresh fairy list to beat `fairy_battle`/`fyb`, use potion `red_tea`/`rt` `green_tea`/`gt`, sell card `sell_card`/`slc`, select server `set_server`/`ss`, friend menu `friend`/`f`, gacha `gacha`/`g`,set free points `point`/`p`, get rewardbox `rewardbox`/`rb`, manually select fairy to beat `fairy_select`/`fs`, re-login `relogin`/`rl`, greet friends `like`/`greet`/`gr`

Expression starts with `t:` means this is a **task**

Append argumentss after `explore`, `sell_card` to specify instant condition, or the action will be performed as what's in `condition` section in config file; `factor_battle` has an optional int arg to specify minimun BC left, default to 0; `fairy_battle` has an optional int arg to specify refresh times, default to `fairy_battle_times` in config file

如：

    login heheh 123456 #login
    set_server cn|set_card factor|factor_battle #set cn server, set carddeck "factor", do factor battle
    ss cn|sc factor|fcb #abbreviation version
    explore 'ooxx' in area.name # explore area "ooxx"
    fcb l:1 70 OR fcb lake:1 70# do factor battle with factor id 1, exit when BC less than 70

Refer to [COMMANDS Document](COMMANDS.en.md) for details

###condition

Globals:

    HH current hour(24-hour format)
    MM current minute
    BC left BC
    BC% left BC as percent, like 0.22
    AP left AP
    AP% left AP as percent, like 0.12
    SUPER super value
    GOLD gold value
    FP friendship point value
    FAIRY_ALIVE whether player's fairy is alive
    GUILD_ALIVE whether guild fairy is alive

PS: You must enter the **fairy list** at once (use `fairy_battle`/`fyb` or `fairy_select`/`fs`) to get the value of `FAIRY_ALIVE` and `GUILD_ALIVE`

PPS: When subject of a expression is single, you can use `$` to replace it.

eg. in `explore_area` expressions, `$.IS_EVENT` and `area.IS_EVENT` are equal

####factor
factor battle expression

values：

`star`: leader card star

`cid`: leader card id

eg:

    start ==1 or star ==2 OR star in [1,2] #leader card star is 1 or 2
    cid in [124,8,256] #leader card id is 124,8 or 256：

####explore_area
area expression, `|` split areas with descending priority, empty to select randomly

values: `area`

properties:

`IS_EVENT`, ~~`IS_DAILY_EVENT`~~, `IS_GUILD`, `NOT_FINNISHED`, `name`

eg.：

    area.IS_EVENT and area.NOT_FINNISHED　#select an event and unfinnished area
    area.name == 'ooooo' #select 'ooooo'
    area.NOT_FINNISHED | area.IS_EVENT #select an unfinnished area; if none, select an event area
    area.NOT_FINNISHED | #select an unfinnished area; if none, select randomly

####explore_floor
area expression, `|` split floors with descending priority, empty to select randomly

values：`floor`

properties：

`NOT_FINNISHED`, `cost`

eg.：

    floor.cost<6 and floor.NOT_FINNISHED #select a floor with cost less than 6 and is unfinnished
    floor.cost<3 | #select a floor with cost less than 3; if none, select randomly

####fairy_select
select which fairies

values：`fairy`

properties：

`IS_MINE`, `LIMIT`(in seconds), `NOT_BATTLED`, `lv`(level), `IS_WAKE`, `IS_WAKE_RARE`, `IS_GUILD`

eg.：

    not fairy.IS_MINE and fairy.LIMIT<600 and fairy.NOT_BATTLED

####fairy_select_carddeck
select which carddeck when encounting a fairy

values：`fairy`

properties：

`lv`, `hp`, `name`, `IS_MINE`, `TIME_LIMIT`(in seconds), `IS_WAKE`, `IS_WAKE_RARE`, `IS_GUILD`

You can only use ternary expressions: `EXP and TRUE-ACTION or FALSE-ACTION` or `TRUE-ACTION if EXP else FALSE-ACTION`, can be nested; card deck name should be wrapped in quote, and is set in **carddeck** section in config file

special carddeck names are:

do not change the carddeck `no_change`, let the fairy escape `letitgo`, abort beating fairy `abort`

eg.：

    fairy.hp>200000 and 'tiandao' or 'full' OR 'tiandao' if fairy.hp>200000 else 'full'　#if fairy hp>200000的, then use carddeck "tiandao", else "full"

####select_card_to_sell
select which cards to sell

values: `card`

properties：

`star`, `lv`, `sid`(serial id), `mid`(card master id)，`price`(sell price), `holo`(is holography card)

eg：

    card.star in [1,2] and card.lv<5 and card.mid != 124 and not card.holo

PS：All **Cherrys** are excluded.