from falcon.errors import HTTPBadRequest as HTTP_Bad_Request, HTTPUnsupportedMediaType as HTTP_Unsupported_Media_Type
from lib.response import *

__all__ = [
    'Bad_Request_Handler',
    'Unsupported_Media_Type_Handler'
]


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


class Unsupported_Media_Type_Handler(Base_Handler):
    error = HTTP_Unsupported_Media_Type
    response = Unsupported_Media_Type_Response
