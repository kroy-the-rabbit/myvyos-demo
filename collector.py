#!/usr/bin/env python3
from vyos import version
import os.path
import psutil
import time
import json
import uuid
import os

## Requests isn't installed on a default VyOS installation
#import requests

import subprocess
from subprocess import Popen

# Create account at myvyos.kroy.io, generate API key
api_key = ""
api_endpoint = "https://myvyos.kroy.io/api"



hostname = "No hostname"

if os.uname()[1] is not None:
    hostname = os.uname()[1]

### System ID would eventually be created and stored in the config file
### For now, just writing out to filesystem for some temporary persistence.  A reboot will obviously wipe this and count this as a new sytem
system_id = uuid.uuid4().hex

if (os.path.exists('/tmp/system.id.txt')):
    system_id = open('/tmp/system.id.txt').read(1000)

with open('/tmp/system.id.txt', 'w') as f:
    f.write(system_id)

print (system_id)

postdata= { 'api_key':api_key, 'stats':{
    'version':version.get_version(),
    'system_id':system_id,
    'root_usage':(psutil.disk_usage('/')[3]),
    'uptime': time.time() - psutil.boot_time(),
    'cpu_percent':psutil.cpu_percent(),
    'mem_percent':(psutil.virtual_memory()[2]),
    'hostname':hostname
    }
 }

#resp = requests.post(api_endpoint,postdata)

## No python-requests, so gotta do this the hard way
with open('/tmp/curlit.sh','w') as f:
    f.write('curl -X POST -H "Content-type: application/json" --data "@/tmp/data.json" ')
    f.write(api_endpoint)

with open('/tmp/data.json', 'w') as f:
    f.write(json.dumps(postdata))


p = Popen(["bash","/tmp/curlit.sh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
output, errors = p.communicate()
print (output)
