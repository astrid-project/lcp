import os

Import_Error = ImportError
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
os.chdir(dir_path)

from about import project, title, version
from api import api
from reader.arg import Arg_Reader
import waitress

db = Arg_Reader.read()

ident = f'{project} - {title} v:{version}'
print(ident)

if db.version is not None:
    print(db.version)
else:
    u, p = db.dev_username, db.dev_password
    waitress.serve(api(title=title, version=version,
                        dev_username=u, dev_password=p),
                   host=db.host, port=db.port, expose_tracebacks=False, ident=ident)
