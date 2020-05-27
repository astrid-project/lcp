from falcon import HTTPBadRequest


class HTTPNotValidJSON(HTTPBadRequest):
    def __init__():
        super(title='Request error', description='Could not decode the request body, either because it was not valid JSON or because it was not encoded as UTF-8.')
