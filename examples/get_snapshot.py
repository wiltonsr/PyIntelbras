# 4.4.2 Get a Snapshot

import sys
import logging
from pyintelbras import IntelbrasAPI

stream = logging.StreamHandler(sys.stdout)
stream.setLevel(logging.DEBUG)
log = logging.getLogger('pyintelbras')
log.addHandler(stream)
log.setLevel(logging.DEBUG)

api = IntelbrasAPI('example.com')
api.login('user', 'pass')

response = api.snapshot(channel=1, type=0)

print(response.status_code)

if response.status_code == 200:
    with open("/tmp/img.jpeg", "wb") as bf:
        bf.write(response.content)
