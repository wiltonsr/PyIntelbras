# 4.10.5 Find Media Files

import re
import sys
import logging
from pyintelbras import IntelbrasAPI

stream = logging.StreamHandler(sys.stdout)
stream.setLevel(logging.DEBUG)
log = logging.getLogger('pyintelbras')
log.addHandler(stream)
log.setLevel(logging.DEBUG)

intelbras = IntelbrasAPI('example.com')
intelbras.login('user', 'pass')

# Step 1 - Create a media files finder.
r = intelbras.mediaFileFind(action='factory.create')
print(r.content.decode())

if r.status_code == 200:

    object_number = re.findall(r'\d+', r.content.decode())[0]

    # Step 2 - Start to find media files satisfied the conditions with the finder.  # noqa: E501
    params = {
        'action': 'findFile', 'object': object_number, 'condition.Channel': 1,
        'condition.StartTime': '2024-8-27 12:00:00',
        'condition.EndTime': '2024-8-29 12:00:00'
    }
    r = intelbras.mediaFileFind(**params)
    print(r.content.decode())

    # Step 3 - Get the media file information found by the finder.
    r = intelbras.mediaFileFind(action='findNextFile',
                          object=object_number, count=100)
    print(r.content.decode())

    # Step 4 - Close the finder.
    r = intelbras.mediaFileFind(action='close', object=object_number)
    print(r.content.decode())

    # Step 5 - Destroy the finder.
    r = intelbras.mediaFileFind(action='destroy', object=object_number)
    print(r.content.decode())

    # 4.10.13 Download Media File with the File Name
    # The file provided here it's just a sample. You must get a real file path from Step 3 # noqa: E501
    r = intelbras.RPC_Loadfile(
        extra_path='/mnt/dvr/2024-08-28/0/dav/02/0/2/371245/02.44.14-02.44.24[R][0@0][0].dav')  # noqa: E501
    print(r)

    if r.status_code == 200:
        with open("/tmp/video.dav", "wb") as bf:
            bf.write(r.content)
