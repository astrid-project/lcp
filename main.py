from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from configparser import ConfigParser
from falcon_auth import FalconAuthMiddleware, BasicAuthBackend
from falcon_apispec import FalconPlugin
from falcon_marshmallow import Marshmallow
from mode import Mode
from resource import *
from schema import *
from swagger_ui import falcon_api_doc
from utils import *
import argparse
import hashlib
import falcon
import json
import waitress


config_parser = ConfigParser()
config_parser.read('config.ini')

title = config_parser.get('info', 'title')
description = config_parser.get('info', 'description')
version = config_parser.get('info', 'version')

lcp_port = config_parser.get('local-control-plane', 'port')
if config_parser.has_option('local-control-plane', 'id'):
    lcp_id = config_parser.get('local-control-plane', 'id')
else:
    lcp_id = None
lcp_mode = config_parser.get('local-control-plane', 'mode')

auth_username = config_parser.get('auth', 'username')
auth_password = config_parser.get('auth', 'password')

cb_endpoint = config_parser.get('context-broker', 'endpoint')
cb_timeout = config_parser.get('context-broker', 'timeout')
cb_username = config_parser.get('context-broker', 'username')
cb_password = config_parser.get('context-broker', 'password')
cb_retry_every_seconds = config_parser.get('context-broker', 'retry-every-seconds')

print(f'{title} v{version}')


parser = argparse.ArgumentParser(
    prog=f'python3 main.py', description=f'{title}: {description}')

parser.add_argument('--port', '-p', type=int,
                    help='TCP Port of the REST Server', default=lcp_port)
parser.add_argument('--id', '-i', type=str, help='ID', default=lcp_id)
parser.add_argument('--mode', '-m', type=str, help='Master mode', choices=['master', 'mode'], default=lcp_mode)

parser.add_argument('--auth-username', '-u', type=str,
                    help='Authorized username', default=auth_username)
parser.add_argument('--auth-password', '-a', type=str,
                    help='Authorized password', default=auth_password)

parser.add_argument('--cb-endpoint', '-c', type=str,
                    help='Context Broker APIs hostname/IP:port', default=cb_endpoint)
parser.add_argument('--cb-timeout', '-b', type=float,
                    help='Context Broker APIs hostname/IP:port', default=cb_timeout)
parser.add_argument('--cb-username', '-r', type=str,
                    help='Authorized username for Context Broker APIs', default=cb_username)
parser.add_argument('--cb-password', '-s', type=str,
                    help='Authorized password for Context Broker APIs', default=cb_password)
parser.add_argument('--cb-retry-every-seconds', '-t', type=int,
                    help='Retry connection to Context Broker APIs every seconds', default=cb_retry_every_seconds)

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
        if username == args.auth_username and hashlib.sha224(password.encode('utf-8')).hexdigest() == args.auth_password:
            return {'username': username}
        else:
            False

    api = falcon.API(middleware=[
        FalconAuthMiddleware(BasicAuthBackend(auth), exempt_routes=['/api/doc', '/api/doc/swagger.json']),
        Marshmallow()
    ])

    api_spec = APISpec(
        title=title,
        version=version,
        openapi_version='2.0',
        produces=['application/json'],
        consumes=['application/json'],
        tags=[{'name': 'status', 'description': 'Status data of the LCP.'},
              {'name': 'code', 'description': 'Code injection at run-time.'},
              {'name': 'config', 'description': 'Configuration at run-time.'}],
        plugins=[
            FalconPlugin(api),
            MarshmallowPlugin(),
        ],
    )

    for schema in BadRequestSchema, UnauthorizedSchema:
        api_spec.components.schema(schema.__name__, schema=schema)

    for Resource in StatusResource, CodeResource, ConfigResource:
        if Resource.request_schema:
            api_spec.components.schema(Resource.request_schema.__class__.__name__, schema=Resource.request_schema)
        if Resource.response_schema:
            api_spec.components.schema(Resource.response_schema.__class__.__name__, schema=Resource.response_schema)

        for route in wrap(Resource.routes):
            resource = Resource(config_parser, args)
            api.add_route(route, resource)
            api_spec.path(resource=resource)

    with open('./api/schema.yaml', 'w') as file:
        file.write(api_spec.to_yaml())

    with open('./api/schema.json', 'w') as file:
        file.write(json.dumps(api_spec.to_dict(), indent=2))

    falcon_api_doc(api, config_path='./api/schema.json', url_prefix='/api/doc', title='API doc')

    waitress.serve(api, host='0.0.0.0', port=args.port)
