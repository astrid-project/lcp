title = 'ASTRID Local Control Plane'
description = 'In each local agent, the control plane is responsible for programmability, i.e., changing the behaviour of the data plane at run-time.'
version = '0.0.1'

print(f'{title} v{version}')

import falcon
import argparse
import waitress

parser = argparse.ArgumentParser(
    prog='python3 main.py', description=title + ': ' + description)
parser.add_argument('--port', '-p', type=int,
                    help='TCP Port of the REST Server', default=4000)
parser.add_argument('--cb-host', '-c', type=str,
                    help='Hostname / IP of the Context Broker APIs REST Server', default='localhost')
parser.add_argument('--cb-port', '-b', type=int,
                    help='TCP Port of the Context Broker APIs REST Server', default=5000)
parser.add_argument('--version', '-v', help='Show version',
                    action='store_const', const=version)

args = parser.parse_args()


from middleware import RequireJSON
from route import Code, Config, Status

api = falcon.API(middleware=[
    Auth(),
    RequireJSON()
])

status = Status(cb_host=args.cb_host, cb_port=args.cb_port)
code = Code(status)
config = Config(status)

api.add_route('/code', code)
api.add_route('/config', config)
api.add_route('/status', status)

if args.version is not None:
    print(args.version)
else:
    host = '0.0.0.0'
    waitress.serve(api, host=host, port=args.port)
