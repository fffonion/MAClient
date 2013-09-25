import random
import clipboard
import sys
import os
sys.path.append(os.path.abspath('..'))
import maclient_network
invid=raw_input('invitation_id >')
while True:
    s=raw_input('session: ').lstrip('S=').strip()
    uname=raw_input('uname: ')
    pwd=raw_input('pwd: ')
    p='invitation_id=%s&login_id=%s&param=&password=%s&param=%s'%(invid,uname,pwd,'35'+(''.join([str(random.randint(0,10)+i-i) for i in range(10)])))
    print maclient_network.encode_param(p)
    clipboard.SetClipboardText(maclient_network.encode_param(p))
    raw_input(maclient_network.encode_param('S=%s&step=%s'%(s,7025)))
    clipboard.SetClipboardText(maclient_network.encode_param('S=%s&step=%s'%(s,7025)))
    raw_input(maclient_network.encode_param('S=%s&step=%s'%(s,8000)))
    clipboard.SetClipboardText(maclient_network.encode_param('S=%s&step=%s'%(s,8000)))
