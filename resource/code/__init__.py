from error.error.http_not_valid_json import HTTPNotValidJson
from resource.base import BaseResource
from resource.code.polycube import injection
from schema.code.request import CodeRequestSchema
from schema.code.response import CodeResponseSchema
from schema.code.response.injected import CodeInjectedResponseSchema
from schema.code.response.error import CodeErrorResponseSchema
from schema.http_error import HTTPErrorSchema
from utils.data import get_data
from utils.datetime import datetime_to_str
from utils.docstring import docstring
from utils.sequence import wrap


class CodeResource(BaseResource):
    request_schema = CodeRequestSchema()
    response_schema = CodeResponseSchema()

    tag = {'name': 'code', 'description': 'Code injection at run-time.'}
    routes = '/code',
    history_filename = f'data/code.history'

    #@docstring(source='code/get.yaml')
    def on_get(self, req, resp):
        req.context['result'] = self.history

    #@docstring(source='code/post.yaml')
    def on_post(self, req, resp):
        json = req.context.get('json', None)
        if json is not None:
            res = dict(when=datetime_to_str(), results=[])
            for data in wrap(json):
                cube, code, interface, output = get_data(code, 'cube', 'code', 'interface')
                if injection(cube, code, interface):
                    output = dict(injected=True, cube=cube, code=code, interface=interface)
                res['results'].append(output)
            req.context['result'] = res
            self.history.append(res)
        else:
            raise HTTPNotValidJson()
