class HTTPConnectionError(HTTPError):
    def __init__(self, connection_error):
        super(title='Connection error',
              description=f'Connection to Polycube at {self.endpoint} not possible.',
              exception=str(connection_error))


class HTTPTimeout(HTTPError):
    def __init__(self, timeout):
       super(title='Polycube Unavailable',
             description=f'Timely response not received from polycube at {self.endpoint} in {ArgReader.db.polycube_request_timeout} seconds.'), exception=str(timeout))


class HTTPRequestException(HTTPRequest):
    def __init__(self, request_exception):
        super((title='Bad request', description=f'Request to Polycube at {self.endpoint} not possible.'),
              exception=str(request_exception))
