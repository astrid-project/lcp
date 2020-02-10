from falcon_auth import FalconAuthMiddleware, BasicAuthBackend
from falcon_marshmallow import Marshmallow
from route import Code, Config, Status
from utils import wrap
import argparse
import falcon
import waitress


config_parser = ConfigParser()
config_parser.read('config.ini')

title = config_parser.get('info', 'title')
description = config_parser.get('info', 'description')
version = config_parser.get('info', 'version')


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
        for route in wrap(RouteResource.route):
            api.add_route(route, RouteResource())

    waitress.serve(api, host='0.0.0.0', port=args.port)
