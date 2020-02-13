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

auth_username = config_parser.get('auth', 'username')
auth_password = config_parser.get('auth', 'password')

cb_endpoint = config_parser.get('context-broker', 'endpoint')
cb_timeout = config_parser.get('context-broker', 'timeout')
cb_username = config_parser.get('context-broker', 'username')
cb_password = config_parser.get('context-broker', 'password')


print(f'{title} v{version}')


parser = argparse.ArgumentParser(
    prog=f'python3 main.py', description=f'{title}: {description}')

parser.add_argument('--port', '-p', type=int,
                    help='TCP Port of the REST Server', default=lcp_port)

parser.add_argument('--auth-username', '-u', type=str,
                    help='Authorized username', default=auth_username)
parser.add_argument('--auth-password', '-a', type=str,
                    help='Authorized password', default=auth_password)

parser.add_argument('--cb-endpoint', '-c', type=str,
                    help='Context Broker APIs hostname/IP:port', default=cb_endpoint)
parser.add_argument('--cb-timeout', '-b', type=str,
                    help='Context Broker APIs hostname/IP:port', default=cb_timeout)
parser.add_argument('--cb-username', '-r', type=str,
                    help='Authorized username for Context Broker APIs', default=cb_username)
parser.add_argument('--cb-password', '-s', type=str,
                    help='Authorized password for Context Broker APIs', default=cb_password)

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
    def auth(username, password):
        return {'username': username} if username == args.auth_username and password == args.auth_password else False

    api = falcon.API(middleware=[
        FalconAuthMiddleware(BasicAuthBackend(auth)),
        Marshmallow()
    ])

    for RouteResource in Status, Code, Config:
        for route in wrap(RouteResource.route):
            api.add_route(route, RouteResource(config_parser, args))

    waitress.serve(api, host='0.0.0.0', port=args.port)
