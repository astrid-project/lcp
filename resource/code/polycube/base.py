from resource.code.polycube.error import HTTPConnectionError, HTTPTimeout, HTTPRequestException
from falcon import HTTPBadRequest, HTTPError, HTTPGatewayTimeout
from requests.exceptions import ConnectionError, RequestException, Timeout
from reader.arg import ArgReader


class Base(object):
   def __init__(endpoint):
      self.endpoint = endpoint

   def error_manager(self, proc):
      try:
         return proc()
      except ConnectionError as conn_err: raise(HTTPConnectionError(conn_err))
      except Timeout as timeout:
         raise(HTTPGatewayTimeout(title='Polycube Unavailable',
                                  description=f'Timely response not received from polycube at {self.endpoint} in {ArgReader.db.polycube_request_timeout} seconds.'))
      except RequestException as req_exp:
         raise(HTTPBadRequest(title='Bad request',
                              description=f'Request to Polycube at {self.endpoint} not possible.'))
