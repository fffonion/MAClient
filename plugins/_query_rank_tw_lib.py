# coding:utf-8
from datetime import datetime
import re
__version__ = 20140221
query_base = 'http://game.ma.mobimon.com.tw:10001/connect/web/revisions_detail?id=%d'
# self.fairy, self.collect, guild.goto, guild.fairy
query_goto = ['http://game.ma.mobimon.com.tw:10001/connect/web/mb_ranklist_fairy?to=%s',
'http://game.ma.mobimon.com.tw:10001/connect/web/mb_ranklist?to=%s',
'http://game.ma.mobimon.com.tw:10001/connect/web/mb_ranklist_guild_fairy?to=%s',
'http://game.ma.mobimon.com.tw:10001/connect/web/mb_ranklist_guild?to=%s']
query_rev = [320, 321, None, None]
# 有效期
query_lifetime = datetime(2014, 3, 6, 18, 0, 0, 0)
now = datetime.now()
#觉醒次数
wake_level = 2
query_title = lambda x: re.findall('class="blanklist comment_news head00">([^<]+)<', x)[0]
query_regex = [
[
('玩家名稱' , lambda x : re.findall('lititle2.*?/span><br[\s/>]*\s+(.*?)\s+<br', x, re.DOTALL)[0]),
('目前排名' , lambda x : re.findall('\d+',re.findall('lititle2.*?/span><br[\s/>]*\s+(.*?)\s+<br', x, re.DOTALL)[1])[0]),
('更新時間' , lambda x : re.findall('\d{4}-\d{2}-\d{2} \d{2}:\d{2}', x)[0]),
('妖精等級加權總和' , lambda x : re.findall('lititle2.*?/span><br[\s/>]*\s+(.*?)\s+<br', x, re.DOTALL)[2]),
('=' , lambda x : ' + '.join(['*'.join(re.findall('>(.*)<',i)[1:3]) for i in re.findall('tr>(.*?)</tr', x, re.DOTALL)[1:1+wake_level]])),
('可见区域排名Up:' , lambda x : ' / '.join(re.findall('td>[\s<p>]*(.*?)[\s</p>]*</td',re.findall('tr>(.*?)</tr', x, re.DOTALL)[7]))),
('               ' , lambda x : ' / '.join(re.findall('td>[\s<p>]*(.*?)[\s</p>]*</td',re.findall('tr>(.*?)</tr', x, re.DOTALL)[8]))),
('               ', lambda x : '......'),
('               ' , lambda x : ' / '.join(re.findall('td>[\s<p>]*(.*?)[\s</p>]*</td',re.findall('tr>(.*?)</tr', x, re.DOTALL)[-2]))),
('          Down:' , lambda x : ' / '.join(re.findall('td>[\s<p>]*(.*?)[\s</p>]*</td',re.findall('tr>(.*?)</tr', x, re.DOTALL)[-1])))
],
[],
[
('玩家名稱' , lambda x : re.findall('lititle2.*?/span><br[\s/>]*\s+(.*?)\s+<br', x, re.DOTALL)[0]),
('所屬公會' , lambda x : re.findall('lititle2.*?/span><br[\s/>]*\s+(.*?)\s+<br', x, re.DOTALL)[1]),
('目前排名' , lambda x : re.findall('\d+',re.findall('lititle2.*?/span><br[\s/>]*\s+(.*?)\s+<br', x, re.DOTALL)[2])[0]),
('更新時間' , lambda x : re.findall('\d{4}-\d{2}-\d{2} \d{2}:\d{2}', x)[0]),
('妖精等級加權總和' , lambda x : re.findall('lititle2.*?/span><br[\s/>]*\s+(.*?)\s+<br', x, re.DOTALL)[3]),
('=' , lambda x : ' + '.join(['*'.join(re.findall('>(.*)<',i)[1:3]) for i in re.findall('tr>(.*?)</tr', x, re.DOTALL)[1:3]])),
],
[]
]
coll = ('收集品數量' , lambda x : re.findall('\d+',re.findall('lititle2.*?/span><br[\s/>]*\s+(.*?)\s+<br', x, re.DOTALL)[2])[0])
query_regex[1] = query_regex[0][:3] + [coll] + query_regex[0][5:]
for p in query_regex[0][5:]:
    query_regex[2].append(p)
query_regex[3] = query_regex[2][:4] + [coll] + query_regex[2][6:]

broswer_headers = {'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'X-Requested-With': 'com.square_enix.million_tw',
                'User-Agent': '',
                'Accept-Language': 'zh-CN, en-US',
                'Accept-Charset': 'utf-8, iso-8859-1, utf-16, *;q=0.7',
                'Referer': 'http://game.ma.mobimon.com.tw:10001/connect/web/'}
