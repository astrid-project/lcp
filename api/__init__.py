from api.spec import Spec
from falcon import API, media
from falcon_auth import FalconAuthMiddleware, BasicAuthBackend
from falcon_marshmallow import Marshmallow
from resource import routes
from swagger_ui import falcon_api_doc
from utils.auth import auth
from utils.json import loads, dumps


def api(title, version, dev_username, dev_password):
    instance = API(middleware=[
        FalconAuthMiddleware(BasicAuthBackend(auth(dev_username, dev_password)),
                             exempt_routes=['/api/doc', '/api/doc/swagger.json']),
        Marshmallow()
    ])

    media_handlers = {
        'application/json': media.JSONHandler(loads=loads, dumps=dumps)
    }
    instance.req_options.media_handlers.update(media_handlers)
    instance.resp_options.media_handlers.update(media_handlers)

    api_spec = Spec(api=instance, title=title, version=version)
    routes(api=instance, spec=api_spec.get())
    falcon_api_doc(instance, config_path='./swagger/schema.json', url_prefix='/api/doc', title='API doc')
    api_spec.write()

    return instance
