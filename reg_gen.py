import ma
import random
import clipboard
while True:
    s=raw_input('session: ').lstrip('S=').strip()
    uname=raw_input('uname: ')
    pwd=raw_input('pwd: ')
    p='invitation_id=8204a&login_id=%s&param=&password=%s&param=%s'%(uname,pwd,'35'+(''.join([str(random.randint(0,10)+i-i) for i in range(10)])))
    print ma.encode_param(p)
    clipboard.SetClipboardText(ma.encode_param(p))
    raw_input(ma.encode_param('S=%s&step=%s'%(s,7025)))
    clipboard.SetClipboardText(ma.encode_param('S=%s&step=%s'%(s,7025)))
    raw_input(ma.encode_param('S=%s&step=%s'%(s,8000)))
    clipboard.SetClipboardText(ma.encode_param('S=%s&step=%s'%(s,8000)))
