import os
import re
import time
import glob
dirpath = 'D:\Dev\Python\Workspace\MAClient'
xml = '<?xml version="1.0" encoding="UTF-8"?><maclient><time>%d</time>' % int(time.time())
p = '<plugin><name>%s</name><version>%s</version><dir>%s</dir></plugin>'
s = '<script><name>%s</name><version>%s</version><dir>%s</dir></script>'
for (pos, temp) in [('', s), ('plugins', p)]:
    for script in glob.glob(os.path.join(dirpath, pos,'*.py')):
        if 'maclient_cli.py' in script or 'maclient_network.py' in script :
            continue
        _s = open(script).read()
        ver = re.findall('__version__[\s=\']*([^\'\s]+)[\']*', _s)
        if ver:
            k = os.path.basename(script)
            xml += temp %(k, ver[0], pos)
open('meta.xml', 'w').write(xml+'</maclient>')