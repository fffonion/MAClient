# coding:utf-8
from _prototype import plugin_prototype
import os, os.path as opath
import math
import time
# start meta
__plugin_name__ = '显示超详细的战斗详情'
__author = 'fffonion'
__version__ = 0.12
__tip__ = '战斗详情加强版已启动'
require_version = 1.70
from cross_platform import *
hooks = {'EXIT__fairy_battle':1}
# extra cmd hook
extra_cmd = {}
# end meta
# 
if PYTHON3:
    _split = lambda x, y = ',':list(map(lambda x:x.decode('utf-8'), x.encode(encoding = 'utf-8').split(y.encode('utf-8'))))
else:
    _split = lambda x, y = ',':x.split(y)

class plugin(plugin_prototype):
    def __init__(self):
        self.skill_names = {}
        self.combo_names = {}

    def load_skill_name(self, loc):
        if PYTHON3:
            f = open(opath.join(getPATH0, 'db/card.%s.txt' % loc), encoding = 'utf8')
        else:
            f = open(opath.join(getPATH0, 'db/card.%s.txt' % loc))
        for c in f.readlines():
            c = _split(c)
            self.skill_names[int(c[0])] = [c[-3], c[-2], c[-1].replace('\n', ' ')]

    def load_combo_names(self, loc):
        if PYTHON3:
            f = open(opath.join(getPATH0, 'db/combo.%s.txt' % loc), encoding = 'utf8')
        else:
            f = open(opath.join(getPATH0, 'db/combo.%s.txt' % loc))
        for c in f.readlines():
            c = _split(c)
            self.combo_names[int(c[0])] = [c[1], int(c[2]), c[3]]

    def EXIT__fairy_battle(self, *args, **kwargs):
        blist = kwargs['pop_extras']('battle_result')
        vs = kwargs['pop_extras']('battle_player')
        if not blist or not vs:
            return
        self.mac_instance = args[0]
        logger = self.mac_instance.logger
        loc = self.mac_instance.loc
        self.carddb = self.mac_instance.carddb
        self.player = self.mac_instance.player
        #self.carddb = kwargs['carddb']
        #self.player = kwargs['player']
        if not self.skill_names:
            self.load_skill_name(loc[:2])
            self.load_combo_names(loc[:2])
        fatk, matk, rnd = 0, 0, 0
        skills = []
        cbos = []
        satk = []
        skill_type = ['0', 'ATK↑', 'HP↑', '3', '4', '5']
        fairy = vs[-1]
        me = vs[0]
        fhp = int(fairy.hp)
        mhp = int(me.hp)
        cur_fhp = fhp
        cur_mhp = mhp
        for l in blist:
            if 'turn' in l:  # 回合数
                rnd = float(l.turn) - 0.5
            else:
                if 'attack_damage' in l:  # 普通攻击
                    if l.action_player == '0':  # 玩家攻击
                        matk += int(l.attack_damage)
                        cur_fhp -= int(l.attack_damage)
                        if cur_fhp < 0:
                            cur_fhp = 0
                    else:  # 妖精攻击
                        fatk += int(l.attack_damage)
                        cur_mhp -= int(l.attack_damage)
                        if cur_mhp < 0:
                            cur_mhp = 0
                        rnd += 0.5  # 妖精回合
                    if l.attack_type not in '12':
                        logger.debug('fairy_battle%satk_type%s' % (_for_debug, l.attack_type))
                if 'special_attack_damage' in l:  # SUPER
                    satk.append(math.ceil(rnd))
                    satk.append(l.special_attack_damage)
                if 'skill_id' in l:
                    # skillcnt+=1
                    if not isinstance(me.card_list, list):
                        me.card_list = [me.card_list]
                    mcard = [c for c in me.card_list if c.master_card_id == l.skill_card ][0]
                    skill_var = l.skill_type == '1' and l.attack_damage or l.skill_hp_player
                    skills.append('%d,%s,%s,%s,%s,%s,%s,%s,%s,%d,%d,%d,%d' % (
                        math.ceil(rnd), skill_type[int(l.skill_type)], skill_var, 
                        self.carddb[int(l.skill_card)][0], mcard.power, mcard.hp, mcard.lv,
                        self.skill_names[int(l.skill_card)][1], self.skill_names[int(l.skill_card)][2],
                        cur_mhp, cur_mhp * 100 / mhp, cur_fhp, cur_fhp * 100 / fhp)
                    )
                    if l.skill_type == '2':#hp:
                        cur_mhp += int(skill_var)
                if 'combo_name' in l:
                    cbos.append('%s,%s,%s,%s(%s)' % (
                        skill_type[int(l.combo_type)],
                        '' if l.combo_hp_player == '0' else l.combo_hp_player,
                        l.combo_name, l.combo_id,
                        int(l.combo_id) in self.combo_names and self.combo_names[int(l.combo_id)][2] or '')
                    )
        if not satk and not cbos and not skills:
            return
        fname = '[%s]%sLv%s_%s_%d%03d.txt' % (self.player.name, args[1].name, args[1].lv, args[1].serial_id, time.time(), ord(os.urandom(1)))
        try:
            cards = ' '.join(map(lambda x:'%s(%s)' % (self.carddb[int(len(x)>4 and self.player.card.sid(x).master_card_id or x)][0],
                str(len(x)>4 and self.player.card.sid(x).master_card_id or x)),
                self.mac_instance._read_config('record', 'last_set_card').strip(',').split(',')))
        except ValueError:
            return
        #    self.mac_instance._read_config('record', 'last_set_card').split(',')))
        if not opath.exists(opath.join(getPATH0, 'battle_details')):
            os.mkdir(opath.join(getPATH0, 'battle_details'))
        if PYTHON3:
            kw = {'encoding' : 'utf-8'}
        else:
            kw = {}
        path = opath.join(getPATH0, 'battle_details', fname)
        with open(path, 'w', **kw) as f:
            f.write('卡组：%s\n' % cards)
            f.write('妖精：%s HP%d LV%s\n' % (args[1].name, fhp, args[1].lv))
            f.write('玩家：HP%d\n' % mhp)
            f.write('ROUND:%d/%d 平均ATK:%.1f/%.1f 伤害:%d 受到伤害:%d\n' % (
                    math.ceil(rnd), math.floor(rnd),
                    matk / math.ceil(rnd), 0 if rnd < 1 else fatk / math.floor(rnd),
                    matk, fatk))
            if satk:
                f.write('咖喱棒：回合%d 伤害%s\n' % (satk[0],satk[1]))
            if cbos:
                f.write('【COMBO】\n类型,数值,ID,名称\n%s\n' % ('\n'.join(cbos)))
            if skills:
                f.write('【技能】\n回合,类型,数值,卡片,ATK,HP,LV,技能名称,技能效果,玩家HP,玩家HP%%,妖精HP,妖精HP%%\n%s' % ('\n'.join(skills)))
        logger.info('battle_result:已保存至 %s' % path)

# def test(a):
#     def do(*args):
#         from xml2dict import XML2Dict
#         from xml2dict import object_dict
#         f = object_dict()
#         f['name'] = '野生米琪特'
#         f['lv'] = '100'
#         f['serial_id'] = '23333'
#         kwargs = {'_extras':{}, 'loc':a['loc'], 'carddb':a['carddb'], 'player':a['player']}
#         ct = XML2Dict.fromstring(open(r'z:/exploration#fairybattle2.xml').read()).response
#         blist = ct.body.battle_battle.battle_action_list
#         kwargs['_extras']['battle_result'] = blist
#         kwargs['_extras']['battle_player'] = ct.body.battle_battle.battle_player_list
#         p = plugin()
#         p.EXIT__fairy_battle(*(None,f), **kwargs)
#     return do