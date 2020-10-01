from api.error_handler import *
from api.media_handler import *
from api.middleware import *
from api.spec import Spec
from falcon import API
from falcon.media import JSONHandler as JSON_Handler, MessagePackHandler as Message_Pack_Handler
from falcon_auth import FalconAuthMiddleware as Falcon_Auth_Middleware
from falcon_elastic_apm import ElasticApmMiddleware as Elastic_Apm_Middleware
from functools import partial
from reader.arg import Arg_Reader
from resource import routes
from swagger_ui import falcon_api_doc
from utils.json import loads, dumps

import falcon

__all__ = [
    'api'
]


def api(title, version, dev_username, dev_password):
    instance = API(middleware=[
        Falcon_Auth_Middleware(Basic_Auth_Backend_Middleware(dev_username, dev_password),
                               exempt_routes=['/api/doc', '/api/doc/swagger.json']),
        Negotiation_Middleware() # ,
        # Elastic_Apm_Middleware(
        #     service_name='lcp-apm',
        #     server_url=Arg_Reader.db.apm_server
        # )
    ])

    media_handlers = {
        falcon.MEDIA_JSON: JSON_Handler(loads=loads,
                                        dumps=partial(dumps, ensure_ascii=False, sort_keys=True)),
        falcon.MEDIA_MSGPACK: Message_Pack_Handler(),
        falcon.MEDIA_XML: XML_Handler(),
        falcon.MEDIA_YAML: YAML_Handler()
    }
    instance.req_options.media_handlers.update(media_handlers)
    instance.resp_options.media_handlers.update(media_handlers)

    instance.add_error_handler(*Bad_Request_Handler.get())
    instance.add_error_handler(*Unsupported_Media_Type_Handler.get())

    api_spec = Spec(api=instance, title=title, version=version)
    routes(api=instance, spec=api_spec.get())
    falcon_api_doc(instance, config_path='./swagger/schema.json',
                   url_prefix='/api/doc', title='API doc')
    api_spec.write()

    return instance
