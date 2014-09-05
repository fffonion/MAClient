Commands are are given in "FULL_VERSION/ABBR_VERSION", while examples are always using full version.

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

###Login

login/l

    login
    login username
    login username password
    

###Set carddeck

set_card/sc

    set_card card_deck_key
    set_card auto_set(CONDITION)

Special deck names are:do not change the carddeck `no_change`, let the fairy escape `letitgo`, abort beating fairy `abort`

`card_deck_key` should appears in section `card_deck`; when `card_deck_key` is **auto_set**, this is equal to `auto_set CONDITION notest`


###Autoset carddeck

auto_set/as

	#All args are optional
	#aim max_dmg:max damage(default)，max_cp:max cp(cp = atk * hp / cost)，defeat:to defeat current fairy(not accurate)
	#line deck lines, select from 1(默认) to 4; it's recommanded to select 1 if aim is  "defeat"
	#fairy if aim is "defeat", then this arg is needed
	#	fairy:15,300000 fairy of level 15 and hp 300000
	#	fairy:15,300000,WAKE fairy of level 15, hp 300000 and wake
	#delta fairy hp delta range(1 by default, AKA no range)
	#bc max: max BC, cur:current BC, or enter a value
	#notest do not save to server after auto_set(ON by default)
    #>carddeck save carddeck to config file with deck name `carddeck`
	#incl include some cards(none by default) (not working)
    auto_set #select carddeck with 1 line, max damage under current BC
	auto_set line:2 bc:max notest #select carddeck with 2 line, max damage under max BC, and save to server
	auto_set aim:defeat line:1 bc:cur fairy:30,263215 notest #select carddeck with 1 line and defeat a fairy of lv 30 and hp 263215, and save
	auto_set aim:max_dmg line:1 bc:cur incl:124 #select carddeck with 1 line and max damage, including Second - Bisclavret, don't save to server
    auto_set aim:max_cp line:1 bc:40 incl:124 > forty
    #select carddeck with 1 line, max CP under cost 40, including Second - Bisclavret, and save to deck name 'forty', don't save to server

###Factor battle

factor_battle/fcb

    factor_battle #select factor randomly
    factor_battle lake:7 #select lake id = 7
    factor_battle lake:7 50 #select lake id = 7, and stop when BC < 50

After enabling plugin `map_factor_lakes`, you can use `mf` command to show connections between lake id and knight card.

###Explore

explore/e

    explore #explore as is configured in 'condition' section
    explore area.name=='學校教室'

Add expression here to override what's configured in config file.


###Fairy list refresh

fairy_battle/fyb

    fairy_battle #refresh fairy list as is configured in 'system' section
    fairy_battle 50 #refresh 50 times

###Use red potion

red_tea/rt

    red_tea
    red_tea / #use the 1/2 red potion

###Use green potion

green_tea/gt

same as red potion

###Sell card

sell_card/slc

###Set server

set_server/ss

    set_server cn
    set_server cn2
    set_server tw

###Friends stuffs

friend/f

Interactive menu

###Gacha

gacha/g

    gacha 1 #friendship gacha
    gacha 2 #gacha ticket gacha
    gacha 4 #11 gacha

###Point setting

point/p

Interactive menu

###Get reward box

reward_box/rb

    reward_box #get all rewards
    reward_box 12345 #get all rewards
    reward_box 1 #get all cards
    reward_box 12 #get all cards and items
    reward_box 3 #only get gold
    reward_box 4 #only get friendship point
    reward_box 5 #only get gacha ticket
    reward_box 5> #only get gacha ticket, and only show total count
    reward_box 5< #attempt to get gacha ticket, but not for real
    reward_box PATTERN #get reward with name matching the PATTERN

Regular expressions are supported

###Manualy select fairy to beat

fairy_select/fs

    fairy_select fairy.lv<60
    fairy_select fairy.lv<60 deck:min #select fairy with lv < 60, use override carddeck 'min'

Add expression here to override what's configured in config file.

Use `deck:xxx` to force use xxx carddeck, or will follow **fairy_select_carddeck** in **condition** section. You can also use auto set:`deck:auto_set(CONDITION)`

###Re-login

relogin/rl

###Greet

like/greet/gr

    like #use default greeting words, if configured in section 'tactic', use that
    like Hi! #say Hi!