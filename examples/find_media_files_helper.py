# 4.10.5 Find Media Files

import re
import sys
import os
import logging
from pyintelbras import IntelbrasAPI

stream = logging.StreamHandler(sys.stdout)
stream.setLevel(logging.DEBUG)
log = logging.getLogger('pyintelbras')
log.addHandler(stream)
log.setLevel(logging.DEBUG)

intelbras = IntelbrasAPI('example.com')
intelbras.login('user', 'pass')


params = {
    'condition.Channel': 1,
    'condition.StartTime': '2024-8-27 12:00:00',
    'condition.EndTime': '2024-8-29 12:00:00'
}

response = intelbras.find_media_files(params)

for item in response.get('items'):
    fp = item.get('FilePath')
    filename = os.path.basename(fp)
    r = intelbras.RPC_Loadfile(extra_path=fp)
    if r.status_code == 200:
        with open(filename, 'wb') as bf:
            bf.write(r.content)
