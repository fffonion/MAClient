# coding:utf-8
import time
import random
from cross_platform import *
from xml2dict import XML2Dict, object_dict
# start meta
__plugin_name__ = '国服公会PVP'
__author = 'fffonion'
__version__ = 0.1
hooks = {}
extra_cmd = {'gpvp':'guild_pvp', 'guild_pvp':'guild_pvp'}

#simple version of _dopost
def _dopost(self, urikey, postdata = '', usecookie = True, setcookie = True, extraheader = {'Cookie2': '$Version=1'}, xmlresp = True, noencrypt = False, savetraffic = False, no2ndkey=False ):
    resp, _dec = self.poster.post(urikey, postdata, usecookie, setcookie, extraheader, noencrypt, savetraffic, no2ndkey)
    self.lastposttime = time.time()
    if int(resp['status']) >= 400:
        return resp, _dec
    resp.update({'error':False, 'errno':0, 'errmsg':''})
    if not xmlresp:
        dec = _dec
    else:
        try:
            dec = XML2Dict.fromstring(_dec).response
        except:
            dec = XML2Dict.fromstring(re.compile('&(?!#)').sub('&amp;',_dec)).response
    try:
        err = dec.header.error
    except:
        pass
    else:
        if err.code != '0':
            resp['errmsg'] = err.message
            # 1050木有BC 1010卖了卡或妖精已被消灭 8000基友点或卡满了 1020维护 1030有新版本
            if not err.code in ['1050', '1010', '1030'] and not (err.code == '1000' and self.loc == 'jp'):  # ,'8000']:
                self.logger.error('code:%s msg:%s' % (err.code, err.message))
                resp.update({'error':True, 'errno':int(err.code)})
        else:
            if not self.player_initiated:
                if self.player.update_all(dec)[1]:
                    self.logger.debug(update_dt[0])
                    open(self.playerfile, 'w').write(_dec)
                    self.logger.debug('post:master cards saved.')
    return resp, dec

def tolist(obj):
    if not isinstance(obj, list):
        if isinstance(obj, unicode):
            return [object_dict({'value':obj})]
        return [obj]
    else:
        return obj

hms = lambda x:x >= 3600 and time.strftime('%H:%M:%S', time.localtime(x + 16 * 3600)) or time.strftime('%M:%S', time.localtime(x))

def guild_pvp(plugin_vals):
    def do(*args):
        self = object_dict()
        #moke the MAClient class
        for k in plugin_vals:
            setattr(self, k, plugin_vals[k])
        self._dopost = lambda *args, **kwargs:_dopost(self, *args, **kwargs)
        self.tolist = tolist
        
        #get guild id
        resp, ct = self._dopost('mainmenu')
        if resp['error']:
            return
        if ct.header.your_data.guild_join_state != '1':
            self.logger.error('你还木有加入公会o(` · ~ · ′。)o ')
            return
        self.guild_id = ct.header.your_data.guild_id
        self.guild_name = ct.header.your_data.guild_name

        #select pvp lake
        PVP_LAKE_ID = -1
        resp, ct = self._dopost('battle/area')
        if resp['error']:
            return
        for l in ct.body.competition_parts.lake:
            if hasattr(l, 'event_id') and int(l.event_id) >= 70:#test
              PVP_LAKE_ID = int(l.event_id)
        if PVP_LAKE_ID == -1:
            self.logger.error('公会PVP湖未找到("▔□▔)')
            return

        #request enemy guild
        resp, ct = self._dopost('battle/guild/lobby', 
            postdata = 'event_id=%s&event_part_id=0&guild_id=%s' % (PVP_LAKE_ID, self.guild_id))
        if resp['error']:
            return
        self.logger.info()
        e_guild = ct.body.guild_battle_info.enemy_guild_info
        m_guild = ct.body.guild_battle_info.my_guild_info
        self.logger.info(('土豪券 剩余%03s\n' % ct.body.ticket_num) + 
            '[%s] Lv.%02s ID:%s\n'
            '本场战斗点数:%03s        累积点数:%03s\n'
            '本场对战记录: %s胜%s败    排名:%s\n'
            '============= VS =============\n'
            '[%s] Lv.%02s ID:%s\n'
            '本场战斗点数:%03s        累积点数:%03s\n'
            '本场对战记录: %s胜%s败    排名:%s' % 
            (
                m_guild.guild_name.center(8), m_guild.guild_level, m_guild.guild_id,
                m_guild.daily_battle_point, m_guild.season_battle_point,
                m_guild.win_count, m_guild.lose_count, m_guild.ranking,
                e_guild.guild_name.center(8), e_guild.guild_level, e_guild.guild_id,
                0 if e_guild.daily_battle_point == {} else e_guild.daily_battle_point, e_guild.season_battle_point,
                e_guild.win_count, e_guild.lose_count, e_guild.ranking
            )
            )

        #request member list
        resp, ct = self._dopost('battle/guild/enemy_member_list', 
            postdata = 'enemy_guild_id=%s&event_id=%s&event_part_id=0&guild_id=%s' % (e_guild.guild_id, PVP_LAKE_ID, self.guild_id))
        if resp['error']:
            return
        e_members = self.tolist(ct.body.enemy_member_list.guild_member)
        #see guild_member_list example
        
        #fuck!
        target = random.choice(e_members)
        resp, ct = self._dopost('battle/guild/battle', 
            postdata = 'battle_type=%s&defender_guild_id=%s&event_id=%s&guild_id=%s&user_id=%s' % 
                (2, e_guild.guild_id, PVP_LAKE_ID, self.guild_id, target.user.id))
        if resp['error']:
            return
        result = ct.body.battle_result
        out_str = []
        if result.winner == '1':
            self.logger.info('YOU WIN 233')
        else:
            self.logger.info('YOU LOSE TAT')
        self.logger.info('G+%s EXP+%s' % (int(result.after_gold) - int(result.before_gold), int(result.before_exp) - int(result.after_exp)))
        if result.after_level != result.before_level:
            self.logger.info('升级了：↑%s' % result.after_level)
        event_result = result.battle_event_result
        self.logger.info('PVP点数:+%s(%s)  倍率:%s  持续时间:%s(%s)' % 
            (event_result.get_point, event_result.battle_point,
            event_result.bonus_rate, hms(int(event_result.bonus_end_time[:-3]) - time.time()),
            time.strftime('%X', time.localtime(int(event_result.bonus_end_time[:-3])))))#[:-3] => /1000
        

    return do

# guild_member_list example
# <battle_class>5</battle_class>
#     <current_time>1409316193</current_time>
#     <rest_battle_time>1409320799</rest_battle_time>
#     <bonus_rate>1</bonus_rate>
#     <bonus_time>0</bonus_time>
#     <ticket_num>77</ticket_num>
#     <enemy_member_list>
#         <guild_member>
#             <user>
#                 <id>376293</id>
#                 <name>
#                     <![CDATA[柚原木实]]> </name>
#                 <country_id>3</country_id>
#                 <cost>190</cost>
#                 <results>
#                     <win>59</win>
#                     <lose>7</lose>
#                 </results>
#                 <town_level>66</town_level>
#                 <next_exp>12748</next_exp>
#                 <leader_card>
#                     <serial_id>1</serial_id>
#                     <master_card_id>650</master_card_id>
#                     <holography>1</holography>
#                     <hp>19272</hp>
#                     <power>17875</power>
#                     <rarity></rarity>
#                     <multiple>1</multiple>
#                     <critical>0</critical>
#                     <lv>100</lv>
#                     <lv_max>100</lv_max>
#                     <exp>322960</exp>
#                     <max_exp>322960</max_exp>
#                     <next_exp>0</next_exp>
#                     <exp_diff>0</exp_diff>
#                     <exp_per>0</exp_per>
#                     <sale_price>226570</sale_price>
#                     <material_price>48000</material_price>
#                     <evolution_price>500</evolution_price>
#                     <plus_limit_count>0</plus_limit_count>
#                     <limit_over>1</limit_over>
#                 </leader_card>
#                 <friends>17</friends>
#                 <friend_max>30</friend_max>
#                 <last_login>12日</last_login>
#                 <ex_gage>45</ex_gage>
#                 <max_card_num>250</max_card_num>
#                 <status_friend>0</status_friend>
#                 <status_yell>1</status_yell>
#                 <count_hunting>0</count_hunting>
#                 <deck_rank>250</deck_rank>
#                 <guild_id>11266</guild_id>
#                 <guild_join_state>1</guild_join_state>
#                 <guild_name>
#                     <![CDATA[唯爱二次元同好会]]> </guild_name>
#             </user>
#             <daily_battle_record>0 胜 0 败</daily_battle_record>
#         </guild_member>
