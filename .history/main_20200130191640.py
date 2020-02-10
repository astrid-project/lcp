from app import app
import argparse
import waitress

parser = argparse.ArgumentParser(
    prog='python3 main.py', description=api.title + ': ' + api.description)
parser.add_argument('--port', '-p', type=int,
                    help='TCP Port of the REST Server', default=5000)

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
