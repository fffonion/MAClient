# coding:utf-8
import httplib2
import hashlib
import random
import json
alphanum = '0123456789abcdef'
verify = lambda x:hashlib.md5("J]KcRe(dxmk5cMS-%sJ]KcRe(dxmk5cMS-" % x).hexdigest()
mac_gen = lambda :':'.join([random.choice(alphanum) + random.choice(alphanum) * (j / j) for j in range(1, 6) ])
mac = mac_gen()
uri = 'mac=%s&verify=%s' % (mac, verify(mac))
print (uri)

a, b = httplib2.Http().request('http://mafama.sinaapp.com/get.php?type=0&%s' % uri, headers =
                            {'Content-Type': 'application/json;charset=gbk',
                            'Connection': 'Keep-Alive',
                            'User-Agent':' Apache-HttpClient/UNAVAILABLE (java 1.4)'}
                            )
b = json.loads(b)
for e in b:
    print ('%s:%s\n' % (e, b[e]))
