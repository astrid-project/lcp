from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from configparser import ConfigParser
from falcon_apispec import FalconPlugin
from falcon_auth import FalconAuthMiddleware, BasicAuthBackend
from falcon_marshmallow import Marshmallow
from mode import Mode
from resource import *
from schema import *
from swagger_ui import falcon_api_doc

import argparse
import falcon
import hashlib
import json
import utils
import waitress


config_parser = ConfigParser()
config_parser.read('config.ini')

title = config_parser.get('info', 'title')
description = config_parser.get('info', 'description')
version = config_parser.get('info', 'version')

lcp_host = config_parser.get('local-control-plane', 'host')
lcp_port = config_parser.get('local-control-plane', 'port')

dev_debug = config_parser.get('dev', 'debug')
dev_username = config_parser.get('dev', 'username')
dev_password = config_parser.get('dev', 'password')


print(f'{title} v{version}')


parser = argparse.ArgumentParser(
    prog=f'python3 main.py', description=f'{title}: {description}')

parser.add_argument('--host', '-o', type=str,
                    help='Hostname/IP of the REST Server', default=lcp_host)
parser.add_argument('--port', '-p', type=int,
                    help='TCP Port of the REST Server', default=lcp_port)

parser.add_argument('--dev-debug', '-d', help='Enable debug',
                    action='store_true')
parser.add_argument('--dev-username', '-u', type=str,
                    help='Authorized username', default=dev_username)
parser.add_argument('--dev-password', '-a', type=str,
                    help='Authorized password', default=dev_password)

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
    args.dev_debug = args.dev_debug or dev_debug

    def auth(username, password):
        auth_data = [(args.dev_username, args.dev_password)]
        auth_data.extends(StatusResource.auth_db)
        if (username, utils.hash(password)) in auth_data:
            return {'username': username}
        else:
            False

    api = falcon.API(middleware=[
        FalconAuthMiddleware(BasicAuthBackend(auth), exempt_routes=[ '/api/doc', '/api/doc/swagger.json' ]),
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

    for Resource in StatusResource, CodeResource, ConfigResource:
        if Resource.request_schema:
            api_spec.components.schema(
                Resource.request_schema.__class__.__name__, schema=Resource.request_schema)
        if Resource.response_schema:
            api_spec.components.schema(
                Resource.response_schema.__class__.__name__, schema=Resource.response_schema)

        for route in utils.wrap(Resource.routes):
            resource = Resource(args)
            api.add_route(route, resource)
            api_spec.path(resource=resource)

    with open('./api/schema.yaml', 'w') as file:
        file.write(api_spec.to_yaml())

    with open('./api/schema.json', 'w') as file:
        file.write(json.dumps(api_spec.to_dict(), indent=2))

    falcon_api_doc(api, config_path='./api/schema.json',
                   url_prefix='/api/doc', title='API doc')

    waitress.serve(api, host=args.host, port=args.port)
