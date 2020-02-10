import falcon

from code import Code
from config import Config
from status import Status

api = falcon.API()
api.title = 'ASTRID Local Control Plane'
api.description = 'In each local agent, the control plane is responsible for programmability, i.e., changing the behaviour of the data plane at run-time.

'

api.add_route('/code', Code())
api.add_route('/config', Config())
api.add_route('/status', Status())
