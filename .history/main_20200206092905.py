from falcon_auth import FalconAuthMiddleware, BasicAuthBackend
from falcon_marshmallow import Marshmallow
from route import Code, Config, Status
from utils import wrap
import argparse
import falcon
import waitress


title = 'ASTRID Local Control Plane'
description = 'In each local agent, the control plane is responsible for programmability, i.e., changing the behaviour of the data plane at run-time.'
version = '0.0.1'

print(f'{title} v{version}')


parser = argparse.ArgumentParser(
    prog=f'python3 {__FILENAME__}', description=f'{title}: {description}')
parser.add_argument('--port', '-p', type=int,
                    help='TCP Port of the REST Server', default=4000)
parser.add_argument('--cb-endpoint', '-c', type=str,
                    help='Context Broker APIs hostname/IP:port', default='localhost:5000')
parser.add_argument('--version', '-v', help='Show version',
                    action='store_const', const=version)

args = parser.parse_args()

if args.version is not None:
    print(args.version)
else:
    api = falcon.API(middleware=[
        FalconAuthMiddleware(BasicAuthBackend(lambda username, password: { 'username': username })),
        Marshmallow()
    ])

    for RouteResource in Status, Code, Config:
        RouteResource.doc_cls.init()
        for route in wrap(RouteResource.route):
            api.add_route(route, RouteResource())

    waitress.serve(api, host='0.0.0.0', port=args.port)
