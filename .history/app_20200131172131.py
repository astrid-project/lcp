import falcon

from middleware import Auth, RequireJSON
from route import Code, Config, Status

api = falcon.API(middleware=[
    Auth(),
    RequireJSON()
])

status = Status()
code = Code(status)
config = Config(status)

api.add_route('/code', code)
api.add_route('/config', config)
api.add_route('/status', status)
