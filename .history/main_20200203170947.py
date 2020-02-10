title = 'ASTRID Local Control Plane'
description = 'In each local agent, the control plane is responsible for programmability, i.e., changing the behaviour of the data plane at run-time.'
version = '0.0.1'

print(f'{title} v{version}')

import falcon
from falcon_auth import FalconAuthMiddleware, BasicAuthBackend
from falcon_marshmallow import Marshmallow
import argparse
import waitress

parser = argparse.ArgumentParser(
    prog='python3 main.py', description=title + ': ' + description)
parser.add_argument('--port', '-p', type=int,
                    help='TCP Port of the REST Server', default=4000)
parser.add_argument('--version', '-v', help='Show version',
                    action='store_const', const=version)

args = parser.parse_args()


from route import Code, Config, Status

api = falcon.API(middleware=[
    FalconAuthMiddleware(BasicAuthBackend(lambda username, password: { 'username': username })),
    Marshmallow()
])

status = Status()
code = Code()
config = Config()

api.add_route('/code', code)
api.add_route('/config', config)
api.add_route('/status', status)

if args.version is not None:
    print(args.version)
else:
    host = '0.0.0.0'
    waitress.serve(api, host=host, port=args.port)
