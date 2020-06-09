from api.media_handler import XMLHandler, YAMLHandler
from api.middleware import NegotiationMiddleware
from api.spec import Spec
from falcon import API, media
from falcon_auth import FalconAuthMiddleware, BasicAuthBackend
from functools import partial
from resource import routes
from swagger_ui import falcon_api_doc
from utils.auth import auth
from utils.json import loads, dumps

import falcon


def api(title, version, dev_username, dev_password):
    instance = API(middleware=[
        FalconAuthMiddleware(BasicAuthBackend(auth(dev_username, dev_password)),
                             exempt_routes=['/api/doc', '/api/doc/swagger.json']),
        NegotiationMiddleware()
    ])

    media_handlers = {
        falcon.MEDIA_JSON: media.JSONHandler(loads=loads,
                                              dumps=partial(dumps, ensure_ascii=False, sort_keys=True)),
        falcon.MEDIA_MSGPACK: media.MessagePackHandler(),
        falcon.MEDIA_XML: XMLHandler(),
        falcon.MEDIA_YAML: YAMLHandler()
    }
    instance.req_options.media_handlers.update(media_handlers)
    instance.resp_options.media_handlers.update(media_handlers)

    api_spec = Spec(api=instance, title=title, version=version)
    routes(api=instance, spec=api_spec.get())
    falcon_api_doc(instance, config_path='./swagger/schema.json',
                   url_prefix='/api/doc', title='API doc')
    api_spec.write()

    return instance
