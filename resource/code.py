from .base import BaseResource

from schema.code.request import CodeRequestSchema
from schema.code.response import CodeResponseSchema
from schema.http_error import HTTPErrorSchema

import atexit
import falcon
import json
import re
import subprocess
import utils


class CodeResource(BaseResource):
    request_schema = CodeRequestSchema()
    response_schema = CodeResponseSchema()

    tag = {'name': 'code', 'description': 'Code injection at run-time.'}
    routes = '/code',
    history_filename = f'data/code.history'

    def on_get(self, req, resp):
        """
        Get the history of injected code.
        ---
        summary: Code injection history
        description: Get the history of injected code.
        tags: [code]
        responses:
            200:
                description: History of the injected code.
                schema:
                    type: array
                    items:
                        oneOf:
                            - CodeInjectedResponseSchema
                            - CodeErrorResponseSchema
            400:
                description: Bad Request.
                schema: HTTPErrorSchema
            401:
                description: Unauthorized.
                schema: HTTPErrorSchema
        """
        req.context['result'] = self.history

    def on_post(self, req, resp):
        """
        Inject code at run-time in the local environment.
        ---
        summary: Code injection
        description: Inject code at run-time in the local environment.
        parameters:
            - name: payload
              required: true
              in: body
              schema:
                type: array
                items: CodeRequestSchema
        tags: [code]
        responses:
            200:
                description: Code injection executed.
                schema: CodeResponseSchema
            400:
                description: Bad Request.
                schema: HTTPErrorSchema
            401:
                description: Unauthorized.
                schema: HTTPErrorSchema
        """
        json = req.context.get('json', None)
        if json is not None:
            res = {
                'when': utils.datetime_to_str(),
                'results': []
            }
            for code in utils.wrap(json):
                name = code.get('name', None)
                src = code.get('source', None)
                if name is None or src is None:
                    output = dict(
                        error=True, description=f'Missing {utils.get_none(name=name, source=src)}')
                else:
                    # TODO inject code
                    output = dict(name=name, injected=True)
                useless_properties = utils.exclude_keys_from_dict(code,
                                                                  'name', 'source')
                if len(useless_properties) > 0:
                    output['warning'] = f'Useless properties: {", ".join(useless_properties.keys())}'
                res['results'].append(output)
            req.context['result'] = res
            self.history.append(res)
        else:
            raise falcon.HTTPBadRequest(title='Request error',
                                        description='Could not decode the request body, either because it was not valid JSON or because it was not encoded as UTF-8.')
