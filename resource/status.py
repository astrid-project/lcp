from datetime import datetime
from docstring import docstring
from falcon.errors import HTTPUnauthorized
from marshmallow.schema import Schema
from reader.arg import ArgReader
from schema.http_error import HTTPErrorSchema
from schema.status import StatusRequestSchema, StatusResponseSchema
from schema.validate import validate
from ttldict import TTLOrderedDict
from utils.datetime import datetime_from_str, datetime_to_str
from utils.hash import generate_username, generate_password, hash
from utils.log import Log
from utils.sequence import wrap

import os


class StatusResource(object):
    auth = dict(exempt_methods=['POST'])
    tag = dict(name='status', description='Status data of the LCP.')
    routes = '/status',
    cb = {}
    auth_db = {}

    def __init__(self):
        """Set the data and logger."""
        cls = StatusResource
        self.data = dict(id=None, started=datetime_to_str(),
                         last_heartbeat=None)
        cls.auth_db = TTLOrderedDict(default_ttl=int(ArgReader.db.auth_max_ttl))
        self.log = Log.get('status')

    def on_get(self, req, resp):
        validate(schema=Schema(), method='GET', data=req.media)
        resp.media = validate(schema=StatusResponseSchema(), method='GET', data=self.data)

    @docstring(source='status/post.yaml')
    def on_post(self, req, resp):
        cls = StatusResource
        req_data = validate(schema=StatusRequestSchema(), method='POST', data=req.media)
        now = datetime_to_str()

        id = req_data.get('id')
        username = req_data.get('username', None)
        password = req_data.get('password', None)

        self.data['id'] = id
        self.data['last_heartbeat'] = now

        if cls.auth_db.get(username, None) != hash(password):
            self.log.warning(f'Credentials from CB {req.host}:{req.port} not valid.')

        username = generate_username()
        password = generate_password()
        cls.auth_db[username] = hash(password)

        self.log.notice(f'hearbeating from CB at {now}')

        resp.media = validate(schema=StatusResponseSchema(), method='POST',
                              data=dict(**self.data, username=username, password=password))
