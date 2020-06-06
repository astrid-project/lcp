import os

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
os.chdir(dir_path)

try:
    from werkzeug.serving import run_with_reloader
    from ttldict import TTLOrderedDict
    from resource.status import StatusResource
    from reader.arg import ArgReader
    from api import api
    import waitress
except ImportError:
    os.system('pip3 install -r requirements.txt')


db = ArgReader.read()

print(f'{db.config.title} version:{db.config.version}')


if db.version is not None:
    print(db.version)
else:
    StatusResource.set(TTLOrderedDict(default_ttl=int(db.auth_max_ttl)))

    @run_with_reloader
    def run_server():
        u, p = db.dev_username, db.dev_password
        waitress.serve(api(title=db.config.title, version=db.config.version,
                           dev_username=u, dev_password=p),
                       host=db.host, port=db.port)

    run_server()
