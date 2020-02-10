from app import app
import argparse
import waitress

parser = argparse.ArgumentParser(
    prog='python3 main.py', description=api.title + ': ' + api.description)
parser.add_argument('--port', '-p', type=int,
                    help='TCP Port of the REST Server', default=5000)

args = parser.parse_args()

host = '0.0.0.0'
waitress.serve(app, host=host, port=args.port)
