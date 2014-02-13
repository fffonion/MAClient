import os
import re
import json
import time
import glob
main_ver = '1.67'
dirpath = 'D:\Dev\Python\Workspace\MAClient'
meta={"time":int(time.time())}
for pos in ['', 'plugins']:
    for script in glob.glob(os.path.join(dirpath, pos,'*.py')):
        _s = open(script).read()
        ver = re.findall('__version__[\s=\']*([^\'\s]+)[\']*', _s)
        if ver:
            k = os.path.basename(script)
            meta[k == 'maclient.py' and 'main' or k] = [ver[0], pos]
_s = open(script).read()
open('meta.json', 'w').write(json.dumps(meta))