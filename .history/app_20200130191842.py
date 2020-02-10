from pyramid.config import Configurator
from pyramid.response import Response


def hello_world(request):
    print('Incoming request')
    return Response('<body><h1>Hello World!</h1></body>')


with Configurator() as config:
    config.add_route('config', '/config')
    config.add_view(hello_world, route_name='config')
    config.add_route('code', '/code')
    config.add_view(hello_world, route_name='code')
    app = config.make_wsgi_app()

app.title = "ASTRID Local Control Plane"
app.description = "TODO" # TODO
app.version = '0.0.1'
