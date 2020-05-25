import os
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
os.chdir(dir_path)

from api import api
from reader.arg import ArgReader
from resource.status import StatusResource
from ttldict import  TTLOrderedDict

import waitress

db = ArgReader.read()

print(f'{db.config.title} version:{db.config.version}')


if db.version is not None:
    print(db.version)
else:
    StatusResource.set(TTLOrderedDict(default_ttl=int(db.auth_max_ttl)))
    waitress.serve(api(title=db.config.title, version=db.config.version,
                       dev_username=db.dev_username, dev_password=db.dev_password),
                    host=db.host, port=db.port)
