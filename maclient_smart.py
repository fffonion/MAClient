#!/usr/bin/env python
# coding:utf-8
# I'm smart, I have magic.
# Contributor:
#      fffonion        <fffonion@gmail.com>
import time
#server specified configutaions
max_card_count_cn=max_card_count_kr=200
max_card_count_tw=max_card_count_jp=250
max_fp_cn=max_fp_kr=10000
max_fp_tw=max_fp_jp=1000000
key_cn=key_tw=key_kr={'res': 'A1dPUcrvur2CRQyl','helper':'A1dPUcrvur2CRQyl','crypt':'rBwj1MIAivVN222b'
    }
key_jp={'res': 'A1dPUcrvur2CRQyl','helper':'A1dPUcrvur2CRQyl','crypt':'uH9JF2cHf6OppaC1'
    }
app_ver_cn=app_ver_kr=100
app_ver_tw=102
app_ver_jp=236
#wake
name_wake_rare=['俠客']
name_wake=name_wake_rare+['觉醒','覺醒','超電磁砲']
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