from resource.base import BaseResource
from schema.code.request import CodeRequestSchema
from schema.code.response import CodeResponseSchema
from schema.code.response.injected import CodeInjectedResponseSchema
from schema.code.response.error import CodeErrorResponseSchema
from schema.http_error import HTTPErrorSchema


class CodeResource(BaseResource):
    request_schema = CodeRequestSchema()
    response_schema = CodeResponseSchema()

    tag = {'name': 'code', 'description': 'Code injection at run-time.'}
    routes = '/code',

    from resource.code.post import on_post
    from resource.code.put import on_put
    from resource.code.delete import on_delete
