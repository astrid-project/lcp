from falcon.errors import HTTPBadRequest as HTTP_Bad_Request
from falcon.errors import HTTPInternalServerError as HTTP_Internal_Server_Error
from falcon.errors import HTTPUnsupportedMediaType as HTTP_Unsupported_Media_Type

from lib.response import Bad_Request_Response, Internal_Server_Error_Response, Unsupported_Media_Type_Response


class Base_Handler(object):
    @classmethod
    def handler(cls, req, resp, ex, params):
        cls.response(exception=ex).apply(resp)
        resp.complete = True

    @classmethod
    def get(cls):
        return cls.error, cls.handler


class Bad_Request_Handler(Base_Handler):
    error = HTTP_Bad_Request
    response = Bad_Request_Response


class Internal_Server_Error_Handler(Base_Handler):
    error = HTTP_Internal_Server_Error
    response = Internal_Server_Error_Response


class Unsupported_Media_Type_Handler(Base_Handler):
    error = HTTP_Unsupported_Media_Type
    response = Unsupported_Media_Type_Response
