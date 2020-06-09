import os

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
os.chdir(dir_path)

try:
    from werkzeug.serving import run_with_reloader
    from reader.arg import ArgReader
    from api import api
    import waitress
except ImportError as error:
    print(error)
    os.system('pip3 install -r requirements.txt')

db = ArgReader.read()

print(f'{db.config.title} version:{db.config.version}')


if db.version is not None:
    print(db.version)
else:
    @run_with_reloader
    def run_server():
        u, p = db.dev_username, db.dev_password
        waitress.serve(api(title=db.config.title, version=db.config.version,
                           dev_username=u, dev_password=p),
                       host=db.host, port=db.port)

    run_server()
