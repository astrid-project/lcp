from app import app, api
import argparse
import waitress

parser = argparse.ArgumentParser(
    prog='python3 main.py', description=api.title + ': ' + api.description)
parser.add_argument('--port', '-p', type=int,
                    help='TCP Port of the REST Server', default=5000)
parser.add_argument('--environment', '-n', choices=['production', 'development'],
                    help='Environment mode', default='production')
parser.add_argument('--version', '-v', help='Show version',
                    action='store_const', const=api.version)
parser.add_argument('--debug', '-d', help='Enable debug', action='store_true')

args = parser.parse_args()

if args.version is not None:
    print(args.version)
else:
    if args.debug:
        if args.environment == 'production':
            print('Debug mode not work in production environment. Use development instead.')
        print(f'Port: {args.port}')
    host = '0.0.0.0'

    if args.environment == 'production':
        waitress.serve(app, host=host, port=5000)
    else:
        app.run(host=host, port=args.port, debug=args.debug, use_reloader=False)
