import falcon
from middleware.auth import Auth
from middleware.require_json import RequireJSON

from code import Code
from config import Config
from status import Status

api = falcon.API(middleware=[
    Auth(),
    RequireJSON()
])

api.add_route('/code', Code())
api.add_route('/config', Config())
api.add_route('/status', Status())
