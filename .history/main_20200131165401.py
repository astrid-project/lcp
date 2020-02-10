from app import api
import argparse
import waitress

title = 'ASTRID Local Control Plane'
description = 'In each local agent, the control plane is responsible for programmability, i.e., changing the behaviour of the data plane at run-time.'
version = 0.0.1

parser = argparse.ArgumentParser(
    prog='python3 main.py', description=title + ': ' + description)
parser.add_argument('--port', '-p', type=int,
                    help='TCP Port of the REST Server', default=5000)
parser.add_argument('--version', '-v', help='Show version',
                    action='store_const', const=version)

args = parser.parse_args()

if args.version is not None:
    print(args.version)
else:
    host = '0.0.0.0'
    waitress.serve(app, host=host, port=args.port)
