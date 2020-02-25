from args import Args
from configparser import ConfigParser
from log import Log
from requests.auth import HTTPBasicAuth

import argparse
import json
import requests

config_parser = ConfigParser()
config_parser.read('config.ini')

title = config_parser.get('info', 'title')
description = config_parser.get('info', 'description')
version = config_parser.get('info', 'version')

lcp_host = config_parser.get('local-control-plane', 'host')
lcp_port = config_parser.get('local-control-plane', 'port')

dev_username = config_parser.get('dev', 'username')
dev_password = 'astrid'

log_level = config_parser.get('log', 'level')

timeout = 20
method = 'get'
path = ''
data = ''

parser = argparse.ArgumentParser(
    prog=f'python3 curl.py', description=f'Custom curl for {title} version {version}')

parser.add_argument('--host', '-i', type=str, help='Hostname/IP', default=lcp_host)
parser.add_argument('--port', '-o', type=int, help='Port', default=lcp_port)

parser.add_argument('--username', '-u', type=str,
                    help='Authorized username', default=dev_username)
parser.add_argument('--password', '-p', type=str,
                    help='Authorized password', default=dev_password)

parser.add_argument('--log-level', '-l', choices=Log.get_levels(),
                    help='Log level', default=log_level)

parser.add_argument('--timeout', '-t', type=float,
                    help='Timeout', default=timeout)
parser.add_argument('--method', '-m', type=str, help='Method', default=method)
parser.add_argument('--path', '-a', type=str, help='Path', default=path)
parser.add_argument('--data', '-d', type=str, help='Request data', default=data)

Args.db = parser.parse_args()

log = Log.get('curl')

try:
    res = getattr(requests, method)(f'http://{Args.db.ip}:{Args.db.port}/{Args.db.path}',
                       auth=HTTPBasicAuth(Args.db.username, Args.db.password),
                       timeout=Args.db.timeout, json=json.loads(Args.db.data))
except ValueError as ve:
    log.debug(ve)
    log.error('not JSON valid data')
except Exception as e:
    log.debug(e)
    log.error(f'connection to {Args.db.ip}:{Args.db.port} not possible')
else:
    try:
        log.info(f'status code: {res.status_code}')
        print(json.dumps(res.json(), indent=2, sort_keys=True))
    except Exception as e:
        log.debug(e)
        log.error('response with not valid JSON')
        print(res.content)
