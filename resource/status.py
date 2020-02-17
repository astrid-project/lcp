# cspell:ignore strftime

from .base import BaseResource
from configparser import ConfigParser
from requests.auth import HTTPBasicAuth
from datetime import datetime
from schema import StatusResponseSchema
import falcon
import requests
import uuid


class StatusResource(BaseResource):
    request_schema = None
    response_schema = StatusResponseSchema()

    routes = '/status',

    def __init__(self, config_parser, args):
        id = config_parser.has_option('local-control-plane', 'id') and config_parser.get(
            'local-control-plane', 'id') or str(uuid.uuid4())
        config_parser.set('local-control-plane', 'id', id)
        with open('config.ini', 'w') as f:
            config_parser.write(f)
        self.data = {
            'id': id,
            'agents': [],
            'started': datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
        }

        for method in ['post', 'put']:
            res = getattr(requests, method)(f'http://{args.cb_endpoint}/config/exec-env',
                                auth=HTTPBasicAuth(args.cb_username, args.cb_password), json={'id': id, 'started': self.data['started']})
            if res.status_code in [requests.codes.ok, requests.codes.created]:
                break
        print(f'with id = {id} from {self.data["started"]}')

    def on_get(self, req, resp):
        """
        Get info about the status of the LCP in the execution environment.
        ---
        summary: Configuration update
        description: Get info about the status of the LCP in the execution environment.
        tags: [status]
        responses:
            200:
                description: Status data of the LCP.
                schema: StatusResponseSchema
            401:
                description: Unauthorized.
                schema: UnauthorizedSchema
        """
        req.context['result'] = self.data
