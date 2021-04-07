import os

Import_Error = ImportError
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
os.chdir(dir_path)

import waitress  # noqa: E402
from rich import pretty, traceback  # noqa: E402
from rich.console import Console  # noqa: E402
from rich.panel import Panel  # noqa: E402

pretty.install()
traceback.install(show_locals=False)

from about import project, title, version  # noqa: E402
from api import api  # noqa: E402
from reader.arg import Arg_Reader  # noqa: E402
from utils.log import Log  # noqa: E402

db = Arg_Reader.read()

if db.version is not None:
    print(db.version)
else:
    ident = f'{project} - {title} v:{version}'
    console = Console()
    console.print(Panel.fit(ident))
    Log.init(config=db.log_config)
    api_instance = api(title=title, version=version)
    Log.get('api').success(f'Accept requests at {db.host}:{db.port}')
    waitress.serve(api_instance, host=db.host, port=db.port, expose_tracebacks=False, ident=ident, _quiet=True)
