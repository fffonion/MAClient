#!/usr/bin/env python
# coding:utf-8
# general registration helper(tw)
# Contributor:
#      fffonion        <fffonion@gmail.com>
import random
import time
import sys
import os
import httplib2
sys.path.append(os.path.abspath('..'))
import maclient_network
import maclient_logging
from xml2dict import XML2Dict
logging = maclient_logging.Logging('logging')
loc=raw_input('server(tw,cn,cn2,cn3) > ') or 'tw'
invid=raw_input('invitation_id > ')
po=maclient_network.poster(loc,logging,'')
cnt=0
while True:
    po.post('check_inspection')
    po.post('notification/post_devicetoken',postdata='S=nosessionid&login_id=&password=&app=and&token=')
    #s=raw_input('session: ').lstrip('S=').strip()
    print po.cookie
    while True:
        uname,pwd='',''
        while len(uname)<4 or len(uname)>14:
            uname=raw_input('uname: ')
        while len(pwd)<8 or len(pwd)>14:
            pwd=raw_input('pwd: ')
        p='invitation_id=%s&login_id=%s&param=&password=%s&param=%s'%(invid,uname,pwd,'35'+(''.join([str(random.randint(0,10)+i-i) for i in range(10)])))
        #print maclient_network.encode_param(p)
        r,d=po.post('regist',postdata=p)
        if(XML2Dict().fromstring(d).response.header.error.code!='0'):
            print(XML2Dict().fromstring(d).response.header.error.message)
            continue
        break
    GET_header=po.header
    GET_header.update({'Cookie':po.cookie})
    #httplib2.Http().request(maclient_network.serv[loc]+'tutorial/next?step=100&resume_flg=1',headers=GET_header)
    time.sleep(2.328374)
    po.post('tutorial/save_character',postdata='country=%s&name=%s'%(random.choice('123'),uname))
    time.sleep(2.123123)
    po.post('tutorial/next',postdata='S=%s&step=%s'%(po.cookie,1000))
    time.sleep(2.123123)
    po.post('tutorial/next',postdata='S=%s&step=%s'%(po.cookie,7025))
    time.sleep(3.123123)
    po.post('tutorial/next',postdata='S=%s&step=%s'%(po.cookie,8000))
    time.sleep(1.232131)
    #httplib2 doesn't follow redirection in POSTs
    resp,ct=httplib2.Http().request(maclient_network.serv[loc]+'mainmenu?fl=1',headers=GET_header)
    if len(ct)>10000:
        cnt+=1
        print('Success. (%d done)'%cnt)
    else:
        print('Error occured.')
    time.sleep(2.232131)
    #po.post('tutorial/next?step=100&resume_flg=1')
    #clipboard.SetClipboardText(maclient_network.encode_param(p))
    #raw_input(maclient_network.encode_param('S=%s&step=%s'%(po.cookie,7025)))
    #clipboard.SetClipboardText(maclient_network.encode_param('S=%s&step=%s'%(po.cookie,7025)))
    #raw_input(maclient_network.encode_param('S=%s&step=%s'%(po.cookie,8000)))
    #clipboard.SetClipboardText(maclient_network.encode_param('S=%s&step=%s'%(po.cookie,8000)))
