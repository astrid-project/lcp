import os

Import_Error = ImportError
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
os.chdir(dir_path)

while True:
    from utils.exception import reload_import
    try:
        from werkzeug.serving import run_with_reloader
        from reader.arg import Arg_Reader
        from api import api
        import waitress
        break
    except Import_Error as error:
        reload_import(error)

db = Arg_Reader.read()

print(f'{db.config.title} version:{db.config.version}')


if db.version is not None:
    print(db.version)
else:
    @run_with_reloader
    def run_server():
        u, p = db.dev_username, db.dev_password
        waitress.serve(api(title=db.config.title, version=db.config.version,
                           dev_username=u, dev_password=p),
                       host=db.host, port=db.port, expose_tracebacks=False)

    run_server()
