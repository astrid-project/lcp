from configparser import ConfigParser
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

lcp_port = config_parser.get('local-control-plane', 'port')

cb_endpoint = config_parser.get('context-broker', 'endpoint')


print(f'{title} v{version}')


parser = argparse.ArgumentParser(
    prog=f'python3 main.py', description=f'{title}: {description}')
parser.add_argument('--port', '-p', type=int,
                    help='TCP Port of the REST Server', default=lcp_port)
parser.add_argument('--cb-endpoint', '-c', type=str,
                    help='Context Broker APIs hostname/IP:port', default=cb_endpoint)
parser.add_argument('--write-config', '-w', help='Write options to config.ini',
                    action='store_true')
parser.add_argument('--version', '-v', help='Show version',
                    action='store_const', const=version)

args = parser.parse_args()

if args.write_config:
    config_parser.set('local-control-plane', 'port', args.port)
    config_parser.set('context-broker', 'endpoint', args.cb_endpoint)
    with open('config.ini', 'w') as f:
            config_parser.write(f)

if args.version is not None:
    print(args.version)
else:
    api = falcon.API(middleware=[
        FalconAuthMiddleware(BasicAuthBackend(
            lambda username, password: {'username': username}))        Marshmallow()
    ])

    for RouteResource in Status, Code, Config:
        for route in wrap(RouteResource.route):
            api.add_route(route, RouteResource(config_parser, args))

    waitress.serve(api, host='0.0.0.0', port=args.port)
