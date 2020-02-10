from .base import BaseResource
from configparser import ConfigParser
from requests import HTTPBasicAuth
from datetime import datetime
from schema import StatusRequest, StatusResponse
import falcon
import requests
import uuid


class StatusResource(BaseResource):
    request_schema = StatusRequest()
    response_schema = StatusResponse()

    route = ['/status']

    def __init__(self, config_parser, args):
        id = config_parser.has_option('local-control-plane', 'id') and config_parser.get(
            'local-control-plane', 'id') or str(uuid.uuid4())
        config_parser.set('local-control-plane', 'id', id)
        with open('config.ini', 'w') as f:
            config_parser.write(f)
        self.data = {
            'id': id,
            'agents': [],
            'alive': datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
        }
        username = config_parser.get('auth', 'username')
        password = config_parser.get('auth', 'password')
        requests.post(f'http://{args.cb_endpoint}/config/exec-env', auth=HTTPBasicAuth(username, password), json={'id': id})
        print(f'with id = {id} from {self.data["alive"]}')

    def on_get(self, req, resp):
        req.context['result'] = self.data
