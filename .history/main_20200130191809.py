from app import app
import argparse
import waitress

parser = argparse.ArgumentParser(
    prog='python3 main.py', description=api.title + ': ' + api.description)
parser.add_argument('--port', '-p', type=int,
                    help='TCP Port of the REST Server', default=5000)
parser.add_argument('--version', '-v', help='Show version',
                    action='store_const', const=api.version)

args = parser.parse_args()

if args.version is not None:
    print(args.version)
else:
    host = '0.0.0.0'
    waitress.serve(app, host=host, port=5000)
