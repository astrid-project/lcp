from functools import partial
from resource import routes

import falcon
from falcon import API
from falcon.media import JSONHandler as JSON_Handler
from falcon.media import MessagePackHandler as Message_Pack_Handler
from falcon_auth import FalconAuthMiddleware as Falcon_Auth_Middleware
from falcon_auth import JWTAuthBackend as JWT_Auth_Backend
from falcon_elastic_apm import ElasticApmMiddleware as Elastic_Apm_Middleware
from falcon_require_https import RequireHTTPS
from swagger_ui import falcon_api_doc

from api.error_handler import Bad_Request_Handler, Internal_Server_Error_Handler, Unsupported_Media_Type_Handler
from api.media_handler import XML_Handler, YAML_Handler
from api.middleware import Negotiation_Middleware
from api.spec import Spec
from reader.arg import Arg_Reader
from utils.json import dumps, loads
from utils.log import Log


def api(title, version):
    log = Log.get('api')

    middlewares = [
        Negotiation_Middleware()
    ]

    if Arg_Reader.db.auth:
        log.notice('JWT authentication enabled')
        middlewares.append(Falcon_Auth_Middleware(JWT_Auth_Backend(user_loader=lambda token: {'user': token},
                                                  secret_key=Arg_Reader.db.auth_secret_key,
                                                  auth_header_prefix=Arg_Reader.db.auth_header_prefix),
                           exempt_routes=['/api/doc', '/api/doc/swagger.json']))
    else:
        log.notice('JWT authentication disabled')

    if Arg_Reader.db.https:
        log.notice('Force to use HTTPS instead of HTTP')
        middlewares.append(RequireHTTPS())
    else:
        log.notice('HTTPS not set')

    if Arg_Reader.db.apm_enabled:
        log.notice('Elastic APM enabled')
        middlewares.append(Elastic_Apm_Middleware(service_name='lcp-apm', server_url=Arg_Reader.db.apm_server))
    else:
        log.notice('Elastic APM disabled')

    instance = API(middleware=middlewares)

    media_handlers = {
        falcon.MEDIA_JSON: JSON_Handler(loads=loads, dumps=partial(dumps, ensure_ascii=False, sort_keys=True)),
        falcon.MEDIA_MSGPACK: Message_Pack_Handler(),
        falcon.MEDIA_XML: XML_Handler(),
        falcon.MEDIA_YAML: YAML_Handler()
    }
    instance.req_options.media_handlers.update(media_handlers)
    instance.resp_options.media_handlers.update(media_handlers)

    instance.add_error_handler(*Bad_Request_Handler.get())
    instance.add_error_handler(*Internal_Server_Error_Handler.get())
    instance.add_error_handler(*Unsupported_Media_Type_Handler.get())

    api_spec = Spec(api=instance, title=title, version=version)
    routes(api=instance, spec=api_spec.get())
    falcon_api_doc(instance, config_path='./swagger/schema.json', url_prefix='/api/doc', title='API doc')
    api_spec.write()

    return instance
