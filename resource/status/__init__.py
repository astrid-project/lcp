from falcon import HTTPUnauthorized
from log import Log
from reader.arg import ArgReader
from schema.http_error import HTTPErrorSchema
from schema.status.response import StatusResponseSchema
from utils.datetime import datetime_to_str
from utils.docstring import docstring
from utils.hash import generate_password, generate_username, hash

import os


class StatusResource(object):
    request_schema = None
    response_schema = StatusResponseSchema()
    auth = dict(exempt_methods=['POST'])
    tag = dict(name='status', description='Status data of the LCP.')
    routes = '/status',
    cb = {}
    auth_db = {}

    def __init__(self):
        """
        Set the data and logger.
        """
        self.data = dict(id=None, started=datetime_to_str(), last_hearthbeat=None)
        self.log = Log.get('status')

    @classmethod
    def set(cls, auth_db):
        """
        Set the authentication db.

        :params cls: StatusResource class
        :auth_db: input db
        """
        cls.auth_db = auth_db

    @docstring(source='status/get.yaml')
    def on_get(self, req, resp):
        req.context['result'] = { **self.data, **dict(auth_db=self.auth_db, cb=self.cb) }

    from resource.status.post import on_post
