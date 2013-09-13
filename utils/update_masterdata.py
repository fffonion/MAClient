import os
import random
import httplib2
import sys
sys.path.append(os.path.abspath('..'))
import maclient
import maclient_logging
os.chdir(os.path.abspath('..'))
sys.path[0]=os.path.abspath('.')
loc='cn'
mac=maclient.maClient(configfile=r'D:\Dev\Python\Workspace\maClient\_mine\config_little.ini')
mac.login()
a,b=mac._dopost('masterdata/card/update',postdata='%s&revision=0'%mac.poster.cookie,noencrypt=True)
open(r'z:\card.%s.txt'%loc,'w').write(b)