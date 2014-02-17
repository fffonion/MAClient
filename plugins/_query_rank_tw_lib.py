# coding:utf-8
from datetime import datetime
import re
__version__ = 20140220
tw_query_base = 'http://game.ma.mobimon.com.tw:10001/connect/web/revisions_detail?id=%d'
tw_query_self_goto = 'http://game.ma.mobimon.com.tw:10001/connect/web/mb_ranklist_fairy?to=%s'
tw_query_guild_goto = 'http://game.ma.mobimon.com.tw:10001/connect/web/mb_ranklist_guild_fairy?to=%s'
# http://game.ma.mobimon.com.tw:10001/connect/web/revisions_detail?id=xxx
# 可以定义多个
tw_query_self_revision = [313]
tw_query_guild_revision = [312]
# 有效期
tw_query_lifetime = datetime(2014, 2, 20, 10, 0, 0, 0)
now = datetime.now()

query_title = lambda x: re.findall('class="blanklist comment_news head00">([^<]+)<', x)[0]
query_self = [
('玩家名稱' , lambda x : re.findall('lititle2.*?/span><br[\s/>]*\s+(.*?)\s+<br', x, re.DOTALL)[0]),
('目前排名' , lambda x : re.findall('\d+',re.findall('lititle2.*?/span><br[\s/>]*\s+(.*?)\s+<br', x, re.DOTALL)[1])[0]),
('更新時間' , lambda x : re.findall('\d{4}-\d{2}-\d{2} \d{2}:\d{2}', x)[0]),
('妖精等級加權總和' , lambda x : re.findall('lititle2.*?/span><br[\s/>]*\s+(.*?)\s+<br', x, re.DOTALL)[2]),
('=' , lambda x : ' + '.join(['*'.join(re.findall('>(.*)<',i)[1:3]) for i in re.findall('tr>(.*?)</tr', x, re.DOTALL)[1:6]])),
('可见区域排名Up:' , lambda x : ' / '.join(re.findall('td>[\s<p>]*(.*?)[\s</p>]*</td',re.findall('tr>(.*?)</tr', x, re.DOTALL)[7]))),
('               ' , lambda x : ' / '.join(re.findall('td>[\s<p>]*(.*?)[\s</p>]*</td',re.findall('tr>(.*?)</tr', x, re.DOTALL)[8]))),
('               ', lambda x : '......'),
('               ' , lambda x : ' / '.join(re.findall('td>[\s<p>]*(.*?)[\s</p>]*</td',re.findall('tr>(.*?)</tr', x, re.DOTALL)[-2]))),
('          Down:' , lambda x : ' / '.join(re.findall('td>[\s<p>]*(.*?)[\s</p>]*</td',re.findall('tr>(.*?)</tr', x, re.DOTALL)[-1])))
]

query_guild = [
('玩家名稱' , lambda x : re.findall('lititle2.*?/span><br[\s/>]*\s+(.*?)\s+<br', x, re.DOTALL)[0]),
('所屬公會' , lambda x : re.findall('lititle2.*?/span><br[\s/>]*\s+(.*?)\s+<br', x, re.DOTALL)[1]),
('目前排名' , lambda x : re.findall('\d+',re.findall('lititle2.*?/span><br[\s/>]*\s+(.*?)\s+<br', x, re.DOTALL)[2])[0]),
('更新時間' , lambda x : re.findall('\d{4}-\d{2}-\d{2} \d{2}:\d{2}', x)[0]),
('妖精等級加權總和' , lambda x : re.findall('lititle2.*?/span><br[\s/>]*\s+(.*?)\s+<br', x, re.DOTALL)[3]),
('=' , lambda x : ' + '.join(['*'.join(re.findall('>(.*)<',i)[1:3]) for i in re.findall('tr>(.*?)</tr', x, re.DOTALL)[1:3]])),
]
for p in query_self[5:]:
    query_guild.append(p)

broswer_headers = {'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'X-Requested-With': 'com.square_enix.million_tw',
                'User-Agent': '',
                'Accept-Language': 'zh-CN, en-US',
                'Accept-Charset': 'utf-8, iso-8859-1, utf-16, *;q=0.7',
                'Referer': 'http://game.ma.mobimon.com.tw:10001/connect/web/'}
