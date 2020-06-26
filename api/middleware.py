from falcon_auth import BasicAuthBackend as Basic_Auth_Backend
from falcon.errors import HTTPUnauthorized as HTTP_Unauthorized
from lib.response import Unauthorized_Response
from resource.status import Status_Resource
from utils.hash import hash
from utils.log import Log

__all__ = [
    'Basic_Auth_Backend_Middleware',
    'Negotiation_Middleware'
]


class Basic_Auth_Backend_Middleware(Basic_Auth_Backend):
    def __init__(self, dev_username, dev_password):
        super().__init__(self.__auth)
        self.dev_username = dev_username
        self.dev_password = dev_password
        self.log = Log.get('basic-auth-backend-extended')

    def authenticate(self, req, resp, resource):
        try:
            return super().authenticate(req, resp, resource)
        except HTTP_Unauthorized as e:
            self.log.exception(e)
            Unauthorized_Response().apply(resp)

    def __auth(self, username, password):
        auth_data = [(self.dev_username, self.dev_password)]
        auth_data.extend(zip(Status_Resource.auth_db.keys(), Status_Resource.auth_db.values()))
        if (username, hash(password)) in auth_data:
            return dict(username=username)
        else:
            return False


class Negotiation_Middleware(object):
    def process_request(self, req, resp):
        resp.content_type = req.content_type
