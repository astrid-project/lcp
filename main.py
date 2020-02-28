from configparser import ConfigParser
config_parser = ConfigParser()
config_parser.read('config.ini')

from log import Log
Log.set_levels(config_parser.items('log'))

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from args import Args
from falcon_apispec import FalconPlugin
from falcon_auth import FalconAuthMiddleware, BasicAuthBackend
from falcon_marshmallow import Marshmallow
from resource import *
from schema import *
from swagger_ui import falcon_api_doc
from ttldict import  TTLOrderedDict

import argparse
import falcon
import hashlib
import json
import utils
import waitress


title = config_parser.get('info', 'title')
description = config_parser.get('info', 'description')
version = config_parser.get('info', 'version')

lcp_host = config_parser.get('local-control-plane', 'host')
lcp_port = config_parser.get('local-control-plane', 'port')

auth_max_ttl = config_parser.get('auth', 'max-ttl')

dev_username = config_parser.get('dev', 'username')
dev_password = config_parser.get('dev', 'password')

log_level = config_parser.get('log', 'level')


print(f'{title} v{version}')


parser = argparse.ArgumentParser(
    prog=f'python3 main.py', description=f'{title}: {description}')

parser.add_argument('--host', '-o', type=str,
                    help='Hostname/IP of the REST Server', default=lcp_host)
parser.add_argument('--port', '-p', type=int,
                    help='TCP Port of the REST Server', default=lcp_port)

parser.add_argument('--auth-max-ttl', '-t', type=str,
                    help='Max authentication db TTL', default=auth_max_ttl)

parser.add_argument('--dev-username', '-u', type=str,
                    help='Authorized username', default=dev_username)
parser.add_argument('--dev-password', '-a', type=str,
                    help='Authorized password', default=dev_password)

parser.add_argument('--log-level', '-l', choices=Log.get_levels(),
                    help='Log level', default=log_level)

parser.add_argument('--write-config', '-w', help='Write options to config.ini',
                    action='store_true')
parser.add_argument('--version', '-v', help='Show version',
                    action='store_const', const=version)

Args.db = parser.parse_args()
for param in 'auth_max_ttl',:
    setattr(Args.db, param, utils.get_seconds(getattr(Args.db, param), to_int=True))

StatusResource.auth_db = TTLOrderedDict(default_ttl=Args.db.auth_max_ttl)

log = Log.get('main')

if Args.db.write_config:
    config_parser.set('local-control-plane', 'port', Args.db.port)
    config_parser.set('context-broker', 'endpoint', Args.db.cb_endpoint)
    with open('config.ini', 'w') as f:
        config_parser.write(f)

if Args.db.version is not None:
    print(Args.db.version)
else:
    def auth(username, password):
        auth_data = [(Args.db.dev_username, Args.db.dev_password)]
        auth_data.extend(zip(StatusResource.auth_db.keys(), StatusResource.auth_db.values()))
        if (username, utils.hash(password)) in auth_data:
            return {'username': username}
        else:
            return False

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
            resource = Resource()
            api.add_route(route, resource)
            api_spec.path(resource=resource)

    with open('./api/schema.yaml', 'w') as file:
        file.write(api_spec.to_yaml())

    with open('./api/schema.json', 'w') as file:
        file.write(json.dumps(api_spec.to_dict(), indent=2))

    falcon_api_doc(api, config_path='./api/schema.json',
                   url_prefix='/api/doc', title='API doc')

    waitress.serve(api, host=Args.db.host, port=Args.db.port)
