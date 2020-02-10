from configparser import ConfigParser
from datetime import datetime
from schema import StatusRequest, StatusResponse
import falcon
import requests
import uuid


class StatusResource(object):
    request_schema = StatusRequest()
    response_schema = StatusResponse()

    route = ['/status']

    def __init__(self, config_parser):
        id = config_parser.has_option('lcp', 'id') and config_parser.get('lcp', 'id') or str(uuid.uuid4())
        config_parser.set('lcp', 'id', id)
        with open('config.ini', 'w') as f:
            config_parser.write(f)
        self.data = {
            'id': id,
            'agents': [],
            'alive': datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
        }
        print(f'with id = {id} from {self.data["alive"]}')

    def on_get(self, req, resp):
        req.context['result'] = self.data
