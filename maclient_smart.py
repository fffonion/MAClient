#!/usr/bin/env python
# coding:utf-8
# I'm smart, I have magic.
# Contributor:
#      fffonion        <fffonion@gmail.com>
import time
import math
import itertools
__version__ = '1.1-build20140128'
# server specified configutaions
max_card_count_cn = max_card_count_kr = max_card_count_tw = max_card_count_jp = 250
max_fp_cn = max_fp_kr = 50000
max_fp_tw = max_fp_jp = 1000000
#key_tw = {'res': 'A1dPUcrvur2CRQyl', 'helper':'A1dPUcrvur2CRQyl', 'crypt':'rBwj1MIAivVN222b'}
key_cn = key_tw = key_kr = {'res': 'A1dPUcrvur2CRQyl', 'helper':'A1dPUcrvur2CRQyl', 'crypt':'011218525486l6u1'}
key_jp = {'res': 'A1dPUcrvur2CRQyl', 'helper':'A1dPUcrvur2CRQyl', 'crypt':'uH9JF2cHf6OppaC1'}
key_rsa_pool = [
"MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBANV2ohKiVs/2cOiGN7TICmQ/NbkuellbTtcKbuDbIlBMocH+Eu0n2nBYZQ2xQbAv+E9na8K2FyMyVY4+RIYEJ+0CAwEAAQ==",
"MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAOLtTe70uQZ2BAneeTyNezMH/yn/uDu6qabQ3XHhmqqW8C4ZLxG7uW6bNmUdZQSUk8dO2+7ZTbN5lQw/u70Av2ECAwEAAQ==",
"MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAM5U06JAbYWdRBrnMdE2bEuDmWgUav7xNKm7i8s1Uy/fvpvfxLeoWowLGIBKz0kDLIvhuLV8Lv4XV0+aXdl2j4kCAwEAAQ==",
"MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAL1mnz5vCQEa1xPeyIUQ2WHIzKIsZp9PKAzJ6etXV2NpyxoGheqlDZ5rXQVLEY2JSY2nBlt/QBdo9xkp8XcFgUsCAwEAAQ==",
"MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAKFTx5sYAmW9kFineXZj6NwGPGA6QSgui+nwb9ru30oeoYviC6e5iHD/Qk7Gc8JPpIA335YHo6K1/U8U9gM3BncCAwEAAQ==",
"MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAL3EP/qaJ9XGmpEia4KqoJkCYFvgpJtWK3zPZ7d/qCF1GbQSSzPI+FUnuJjAXSZ43vvYYmQNHNYg791C9SrSOT0CAwEAAQ==",
"MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBANWNwx1kRSlR5sl3dHkPtW//F5KlRQMPWbrLG3ZyCI1q3NUMOC+xdC87gGiINs4WC3S28j0/DrrocIXS7zf2MdECAwEAAQ==",
"MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBANzMvdAQ/lmyAQQ3S0B1BkzlwvR8mYrCiATLRV0t/HeudLvhUgbkWm2UNr4M84f0wA52XqFPABMyp+o59D4DEwUCAwEAAQ==",
"MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBANr/4m+Z7qKlr2kmyZmgNjf49LSgm6QP5JZwk+Wi2m8E68sUMyfKkhr1t2OXlvNAEfQrSYHu6rlXqpSf2o1zvSkCAwEAAQ==",
"MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBANqJlJznVfrsXd/Nnn4L7E7Kcz2u1YwIExrJC3uyxsEk+HiCnNJ8ZUFtkc7XeZKEyw2UFfiQ73SOFAzhVfkCCS0CAwEAAQ==",
]

app_ver_cn = 102
app_ver_tw = 200
app_ver_kr = 105
app_ver_jp = 250
# wake
name_wake_rare = '年獸比南珊'
# snda gplus, not working
class snda_gplus():
    # thanks to luw2007(https://github.com/luw2007/libMA/blob/master/push.py)
    # 心跳时间
    beat_timeout = 100
    DES_KEY = "Fwe3;$84@kl3221554*G(|d@"
    ACTIVE_URL = "http://push.mam.sdo.com:8000/active.php"
    # 推送认证
    push_verify = b'\x0200890001{deviceToken}\x03{token}\x03{timepos}\x04'
    # 推送确认
    push_response = b'\x02002000054037749042\x04'
    # 心跳包
    push_beat = b'\x0200100007\x04'
    def __init__(self):
        import threading
        #from Crypto.Cipher import DES3
        pass
    def check_push(self):
        pass

# fake android
def gen_android_id(seed = time.time()):
    pass

def gen_imei(seed = time.time()):
    pass


# platform specified config enhancer
class config_changer():
    pass

class calc():
    WAKE_FAIRY, NORMAL_FAIRY = True, False
    NORMAL_FAIRY_1, NORMAL_FAIRY_2, WAKE_FAIRY, RARE_FAIRY = 0, 1, 2, 3

    @classmethod
    def items_get(cls, fairy_lv, is_wake = False, damage_hp = 0):
        '''
        收集品获得量计算器
        '''
        fairy_lv = int(fairy_lv)
        # 计算妖精预测血量
        fairy_hp = calc.fairy_hp(fairy_lv, is_wake)
        # =0为一击打败
        if damage_hp == 0:
            damage_hp = fairy_hp
        # 分两种情况
        i = is_wake and ((1000 + fairy_lv * 40) * damage_hp / fairy_hp) or ((10 * fairy_lv) * damage_hp / fairy_hp)
        # 向上取整，取10的倍数
        return int(math.ceil(i / 10.0) * 10)

    @classmethod
    def fairy_hp(cls, lv, wake = False):
        '''
        妖精预测血量计算器
        '''
        return wake and 26662 * (lv + 25) or 7783 * (lv + 2)
        # return wake and 30618*(lv+25) or 7783*(lv+2)

    @classmethod
    def fairy_atk(cls, lv, type = 0):
        '''
        妖精预测平均攻击计算器
        '''
        # data required
        # 普妖(一般)有两种，另外有醒妖和稀有妖
        return (int(lv) - 2) * 400

def _defeat(fairy, delta, show = False):
    def _detail(side):
        sides = ['FAIRY', 'YOU']
        print('%-5s:' % (sides[side]))
    fatk = calc.fairy_atk(fairy.lv, type = fairy.IS_WAKE)
    fhp = fairy.hp
    if show:
        detail = _detail
    else:
        detial = lambda x:None
    ####↑以上为静态数据###↓以下为卡组计算数据######
        def do(atkl, hp, rnd):
            # global t1
            # t1-=time.time()
            # 计算当妖精打死玩家时玩家对妖精的伤害
            dmg = 0
            for one_atk in itertools.cycle(atkl):
                dmg += one_atk
                if dmg >= fairy.hp * delta:
                    # t1+=time.time()
                    return True
                hp -= fatk
                if hp <= 0:
                    # t1+=time.time()
                    return False
    return do

HP, ATK, LV, MID, SID = 0, 1, 2, 3, 4

def _carddeck_info(cards):
    '''
    卡组的atk，hp，排数
    '''
    # 卡组攻击
    _hp = sum(map(lambda d:d[HP], cards))
    # 卡组攻击轮数
    _rnd = int(math.ceil(1.0 * len(cards) / 3))
    # 卡组攻击
    _atk = [0, ] * _rnd
    for i in range(_rnd):
        # 每排的攻击
        _atk[i] = sum(map(lambda d:d[ATK], cards[i * 3:min(i * 3 + 3, len(cards))]))
    return _atk, _hp, _rnd

# card_deck generator
DEFEAT, MAX_DMG, MAX_CP = 0, 1, 2
def carddeck_gen(player_cards, aim = DEFEAT, bclimit = 999, includes = [], maxline = 2, seleval = 'True', fairy_info = None, delta = 1, fast_mode = False):
    '''
    自动配卡
    aim 目标
    bclimit 最大BC
    seleval 优选卡
    !includes 必须有这些卡（card对象）
    player_cards cards实例
    fairy_info 妖精信息，hp，lv
    range 允许误差（预测伤害相对于妖精血量）
    maxline 最大排数
    '''
    # print(aim,bclimit,includes,maxline,seleval,fairy_info,delta)
    # 只需要hp,atk,lv,cost,master_card_id,serial_id,object_dict->list节省20%时间
    _cards = [(
            card.hp,
            card.power,
            card.lv,
            card.master_card_id,
            card.serial_id)
        for card in player_cards.cards if eval(seleval)]  # 减少待选卡片数
    print('Selecting cards from %s candidates...' % len(_cards))
    _iter_gen = lambda cardnum = 3:itertools.combinations(_cards, cardnum)
    _sumup = lambda a, b:a + b
    atkpw = lambda d:d[HP] + d[ATK]
    cp = lambda d:1.0 * (d[HP] + d[ATK]) / player_cards.db[d[MID]][2]
    reslist = []
    if aim == DEFEAT:
        if not fairy_info:
            return ['没有输入妖精信息']
        dcalc = _defeat(fairy_info, delta, show = False)
        for deckcnt in [1, 2] + [i * 3 for i in range(1, maxline + 1)]:
            last_failed = 0
            for deck in _iter_gen(deckcnt):
                mids = map(lambda d: d[MID], deck)
                if deckcnt != len(list(set(mids))):  # 有重复卡的跳过
                    continue
                _cost = sum(map(lambda e:player_cards.db[e][2], mids))
                if _cost > bclimit:  # BC太多了跳过
                    continue
                _atk, _hp, _rnd = _carddeck_info(deck)
                if last_failed > (sum(_atk) * _hp):
                     continue
                if dcalc(_atk, _hp, _rnd):  # 看能不能打败
                    sids = map(lambda d: d[SID], deck)
                    # print sids
                    reslist.append([1.0 * (sum(_atk) + _hp) / _cost, _atk, _hp, _cost, sids, mids])
                else:
                    if last_failed < (sum(_atk) * _hp):
                        last_failed = (sum(_atk) * _hp)
            # 若当前数量的卡组能满足要求，则不找更多的卡了
            if reslist:
                break
        # COST最小，其次看CP
        return_lambda = lambda x:(-x[3], x[0])
    elif aim == MAX_DMG or aim == MAX_CP:
        if aim == MAX_DMG:
            deckcnts = [i * 3 for i in range(maxline, 0, -1)] + [1, 2]
            return_lambda = lambda x:(sum(x[0]) * x[1])
            _cards = sorted(_cards, key = lambda x:x[ATK] * x[HP], reverse = True)  # [:min(3*maxline+3,len(_cards))]
            # _cards=sorted(_cards,key=lambda x:x[ATK]*x[HP]/player_cards.db[x[MID]][2],reverse=True)[:len(_cards)/2]
        else:
            deckcnts = [i * 3 for i in range(1, maxline + 1)] + [1, 2]
            return_lambda = lambda x:(1.0 * (x[1] * sum(x[0])) / x[2])
            _cards = sorted(_cards, key = lambda x:x[ATK] * x[HP] / player_cards.db[x[MID]][2], reverse = True)  # [:min(3*maxline+3,len(_cards))]
        if fast_mode:
            _cards = _cards[:min(3 * maxline + 6, len(_cards))]
        for deckcnt in deckcnts:
            for deck in _iter_gen(deckcnt):
                mids = map(lambda d: d[MID], deck)
                _cost = sum(map(lambda e:player_cards.db[e][2], mids))
                if bclimit >= _cost:
                    _atk, _hp, _rnd = _carddeck_info(deck)
                    sids = map(lambda d: d[SID], deck)
                    reslist.append([_atk, _hp, _cost, sids, mids])
            if reslist:
                break
    # for r in reslist:
    #     print r,','.join(map(lambda e: player_cards.db[e][0],r[2]))
    # 返回cost,sid，mid
    # 错误时返回[errmsg]
    if reslist:
        print ('Found %d suitable carddeck(s).' % len(reslist))
        r = max(reslist, key = return_lambda)
        return r[-5:]
    else:
        return ['未能选出符合条件的卡组']


if __name__ == '__main__':
    print(calc.fairy_hp(1, calc.NORMAL_FAIRY))
    print(calc.items_get(7, calc.WAKE_FAIRY, 505956))
