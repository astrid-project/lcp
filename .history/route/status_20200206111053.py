from configparser import ConfigParser
from datetime import datetime
from schema import StatusRequest, StatusResponse
import falcon
import uuid


class StatusResource(object):
    request_schema = StatusRequest()
    response_schema = StatusResponse()

    route = ['/status']

    def __init__(self, config_parser):
        config_parser = config_parser
        id = config_parser.has() config.get('lcp', 'id')

        self.data = {
            'id': ,
            'agents': [],
            'alive': datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
        }

    def on_get(self, req, resp):
        req.context['result'] = self.data
