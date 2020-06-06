from falcon.errors import HTTPBadRequest, HTTPGatewayTimeout, HTTPServiceUnavailable
from requests.exceptions import ConnectionError, Timeout
from reader.arg import ArgReader
from utils.log import Log


def request_manager(self, resp_req):
    try:
        resp_req.raise_for_status()

    except ConnectionError as conn_err:
        self.log.error(f'Exception: {conn_err}')
        if resp_req.content:
            self.log.error(f'Response: {resp_req.content}')

        raise HTTPServiceUnavailable(
            title='Connection error',
            description=f'Connection to Polycube at {self.endpoint} not possible.')

    except Timeout as timeout:
        self.log.error(f'Exception: {timeout}')
        if resp_req.content:
            self.log.error(f'Response: {resp_req.content}')

        to = ArgReader.db.polycube_timeout
        raise HTTPGatewayTimeout(
            title='Polycube Unavailable',
            description=f'Timely response not received from polycube at {self.endpoint} in {to} seconds.')
