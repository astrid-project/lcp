from datetime import datetime
from docstring import docstring
from falcon.errors import HTTPUnauthorized as HTTP_Unauthorized
from lib.http import HTTP_Method
from lib.response import *
from schema.response import *
from marshmallow.schema import Schema
from reader.arg import Arg_Reader
from schema.status import *
from ttldict import TTLOrderedDict as TTL_Ordered_Dict
from utils.datetime import datetime_from_str, datetime_to_str
from utils.hash import generate_username, generate_password, hash
from utils.log import Log
from utils.sequence import is_list, wrap

import os


__all__ = [
    'Status_Resource'
]


class Status_Resource(object):
    auth = dict(exempt_methods=['POST'])
    tag = dict(name='status', description='Status data of the LCP.')
    routes = '/status',
    cb = {}
    auth_db = {}

    def __init__(self):
        """Set the data and logger."""
        cls = Status_Resource
        self.data = dict(id=None, started=datetime_to_str(),
                         last_heartbeat=None)
        ttl = int(Arg_Reader.db.auth_max_ttl)
        cls.auth_db = TTL_Ordered_Dict(default_ttl=ttl)
        self.log = Log.get('status')

    @docstring(source='status/get.yaml')
    def on_get(self, req, resp):
        resp_data, valid = Status_Response_Schema(method=HTTP_Method.GET) \
            .validate(data=self.data)
        if valid:
            resp_data, valid = Status_Response_Schema(method=HTTP_Method.GET) \
                .validate(data=self.data)
            if valid:
                Content_Response(self.data).apply(resp)
            else:
                resp_data.apply(resp)
        else:
            resp_data.apply(resp)

    @docstring(source='status/post.yaml')
    def on_post(self, req, resp):
        req_data = req.media or {}
        resp_data, valid = Status_Request_Schema(method=HTTP_Method.POST)  \
            .validate(data=req_data)
        if valid:
            now = datetime_to_str()

            id = req_data.get('id')
            username = req_data.get('username', None)
            password = req_data.get('password', None)

            self.data['id'] = id
            self.data['last_heartbeat'] = now

            if username and self.auth_db.get(username, None) != hash(password):
                msg = f'Credentials from CB {req.host}:{req.port} not valid.'
                self.log.warning(msg)

            username = generate_username()
            password = generate_password()
            self.auth_db[username] = hash(password)

            self.log.notice(f'hearbeating from CB at {now}')

            data = dict(**self.data, username=username, password=password)
            resp_data, valid = Status_Response_Schema(method=HTTP_Method.POST) \
                .validate(data=data)
            if valid:
                Content_Response(data).apply(resp)
            else:
                resp_data.apply(resp)
        else:
            resp_data.apply(resp)
