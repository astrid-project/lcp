import falcon
from config import Config
from status import Status
from code import Code

api = falcon.API()

api.add_route('/code', Code())
api.add_route('/config', Config())
api.add_route('/status', Status())
