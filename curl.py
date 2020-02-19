import argparse
from configparser import ConfigParser
from requests.auth import HTTPBasicAuth
import json
import requests

config_parser = ConfigParser()
config_parser.read('config.ini')

title = config_parser.get('info', 'title')
description = config_parser.get('info', 'description')
version = config_parser.get('info', 'version')

ip = 'localhost'
port = config_parser.get('local-control-plane', 'port')
username = config_parser.get('auth', 'username')
password = 'astrid'
timeout = 20
method = 'get'
path = ''
data = ''

parser = argparse.ArgumentParser(
    prog=f'python3 curl.py', description=f'Custom curl for {title} version {version}')

parser.add_argument('--ip', '-i', type=str, help='IP', default=ip)
parser.add_argument('--port', '-o', type=int, help='Port', default=port)
parser.add_argument('--username', '-u', type=str,
                    help='Authorized username', default=username)
parser.add_argument('--password', '-p', type=str,
                    help='Authorized password', default=password)
parser.add_argument('--timeout', '-t', type=float,
                    help='Timeout', default=timeout)
parser.add_argument('--method', '-m', type=str, help='Method', default=method)
parser.add_argument('--path', '-a', type=str, help='Path', default=path)
parser.add_argument('--data', '-d', type=str, help='Request data', default=data)

args = parser.parse_args()

try:
    res = getattr(requests, method)(f'http://{args.ip}:{args.port}/{args.path}',
                       auth=HTTPBasicAuth(args.username, args.password), timeout=args.timeout, json=args.data)
except:
    print(f'Error: connection to {args.ip}:{args.port} not possible.')
else:
    try:
        print(f'Status code: {res.status_code}.')
        print(json.dumps(res.json(), indent=2, sort_keys=True))
    except:
        print('\nError: response with not valid JSON.')
        print(res.content)
