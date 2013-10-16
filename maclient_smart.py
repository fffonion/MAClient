#!/usr/bin/env python
# coding:utf-8
# I'm smart, I have magic.
# Contributor:
#      fffonion        <fffonion@gmail.com>
import time
import math
#server specified configutaions
max_card_count_cn=max_card_count_kr=200
max_card_count_tw=max_card_count_jp=250
max_fp_cn=max_fp_kr=10000
max_fp_tw=max_fp_jp=1000000
key_cn=key_tw=key_kr={'res': 'A1dPUcrvur2CRQyl','helper':'A1dPUcrvur2CRQyl','crypt':'rBwj1MIAivVN222b'
    }
key_jp={'res': 'A1dPUcrvur2CRQyl','helper':'A1dPUcrvur2CRQyl','crypt':'uH9JF2cHf6OppaC1'
    }
app_ver_cn=101
app_ver_tw=102
app_ver_kr=100
app_ver_jp=236
#wake
name_wake_rare=['禁書目錄']
name_wake=name_wake_rare+['觉醒','覺醒','雷蒂麗']
#snda gplus
class snda_gplus():
    #thanks to luw2007(https://github.com/luw2007/libMA/blob/master/push.py)
    #心跳时间
    beat_timeout = 100
    DES_KEY = "Fwe3;$84@kl3221554*G(|d@"
    ACTIVE_URL = "http://push.mam.sdo.com:8000/active.php"
    #推送认证
    push_verify = b'\x0200890001{deviceToken}\x03{token}\x03{timepos}\x04'
    #推送确认
    push_response = b'\x02002000054037749042\x04'
    #心跳包
    push_beat = b'\x0200100007\x04'
    def __init__(self):
        import threading
        from Crypto.Cipher import DES3
        pass
    def check_push(self):
        pass

#fake android
def gen_android_id(seed=time.time()):
    pass

def gen_imei(seed=time.time()):
    pass

#card_deck generator
def carddeck_gen(player):
    pass

#platform specified config enhancer
class config_changer():
    pass

class calc():
    WAKE_FAIRY,NORMAL_FAIRY=True,False
    NORMAL_FAIRY_1,NORMAL_FAIRY_2,WAKE_FAIRY,RARE_FAIRY=0,1,2,3

    @classmethod
    def items_get(cls,fairy_lv,is_wake=False,damage_hp=0):
        '''
        收集品获得量计算器
        '''
        fairy_lv=int(fairy_lv)
        #计算妖精预测血量
        fairy_hp=calc.fairy_hp(fairy_lv,is_wake)
        #=0为一击打败
        if damage_hp==0:
            damage_hp=fairy_hp
        #分两种情况
        i=is_wake and ((1000+fairy_lv*40)*damage_hp/fairy_hp) or ((10*fairy_lv)*damage_hp/fairy_hp)
        #向上取整，取10的倍数
        return int(math.ceil(i/10.0)*10)

    @classmethod
    def fairy_hp(cls,lv,wake=False):
        '''
        妖精预测血量计算器
        '''
        return wake and 26662*(lv+25) or 7783*(lv+2)
        #return wake and 30618*(lv+25) or 7783*(lv+2)

    @classmethod
    def fairy_atk(cls,lv,type=0):
        '''
        妖精预测平均攻击计算器
        '''
        #data required
        #普妖(一般)有两种，另外有醒妖和稀有妖
        pass


if __name__=='__main__':
    print calc.fairy_hp(1,calc.NORMAL_FAIRY)
    print calc.items_get(7,calc.WAKE_FAIRY,505956)