import falcon

from middleware import Auth, RequireJSON
from route import Code, Config, Status

print('ASTRID Local Plane')

api = falcon.API(middleware=[
    Auth(),
    RequireJSON()
])

api.add_route('/code', Code())
api.add_route('/config', Config())
api.add_route('/status', Status())
