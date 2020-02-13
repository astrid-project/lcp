# cspell:ignore strftime

from .base import BaseResource
from datetime import datetime
from utils import wrap, get_none
from schema import CodeRequest, CodeResponse
import falcon
import re
import subprocess


class CodeResource(BaseResource):
    request_schema = CodeRequest()
    response_schema = CodeResponse()

    route = ['/code']

    def on_post(self, req, resp):
        json = req.context.get('json', None)
        if json is not None:
            res = {
                'when': datetime.now().strftime("%Y/%m/%d-%H:%M:%S"),
                'results': []
            }
            for code in wrap(json):
                name = code.get('name', None)
                src = code.get('source', None)
                if name is None or src is None:
                    output = dict(error=True, description=f'Missing {get_none(name=name, source=src)}')
                else:
                    # TODO inject code
                    output = dict(name=name, injected=True)
                useless_properties = exclude_keys_from_dict(code, 'name', 'source')
                if len(useless_properties) > 0:
                    output['warning'] = f'Useless properties: {", ".join(useless_properties.keys())}'
            res['results'].append(output)
        else:
            raise falcon.HTTPBadRequest(title="Request error", description="Empty request")
