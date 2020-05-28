from resource.code.polycube.error import HTTPConnectionError, HTTPTimeout, HTTPRequestException
from requests.exceptions import ConnectionError, RequestException, Timeout
from reader.arg import ArgReader


class Base(object):
   def __init__(endpoint):
      self.endpoint = endpoint

   def error_manager(self, proc):
      try:
         return proc()
      except ConnectionError as conn_err: raise(HTTPConnectionError(conn_err))
      except Timeout as timeout:  raise(HTTPTimeout(expr=timeout))
      except RequestException as req_exp: raise(HTTPRequestException(reg_exp))
