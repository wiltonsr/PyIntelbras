# 4.5.6 [Config] Channel Title

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

response = api.configManager(action='getConfig', name='ChannelTitle')

print(response.status_code)
print(response.content.decode())
