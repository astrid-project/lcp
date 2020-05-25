from datetime import datetime
from log import Log
from reader.arg import ArgReader
from requests.auth import HTTPBasicAuth
from schema.http_error import HTTPErrorSchema
from schema.status.response import StatusResponseSchema

import falcon
import hashlib
import os
import requests
import threading
import utils
import uuid


class StatusResource(object):
    request_schema = None
    response_schema = StatusResponseSchema()

    auth = {
        'exempt_methods': ['POST']
    }

    tag = {'name': 'status', 'description': 'Status data of the LCP.'}
    routes = '/status',
    cb = {}
    auth_db = {}

    def __init__(self):
        """
        Set the data and logger.
        """
        self.data = {
                'id': None,
                'started': utils.datetime_to_str(),
                'last_hearthbeat': None
            }
        self.log = Log.get('status')

    @classmethod
    def set(cls, auth_db):
        """
        Set the authentication db.

        :params cls: StatusResource class
        :auth_db: input db
        """
        cls.auth_db = auth_db

    def on_get(self, req, resp):
        """
        Get info about the status of the LCP in the execution environment.
        ---
        summary: Status info
        description: Get info about the status of the LCP in the execution environment.
        tags: [status]
        responses:
            200:
                description: Status data of the LCP.
                schema: StatusResponseSchema
            401:
                description: Unauthorized.
                schema: HTTPErrorSchema
        """
        req.context['result'] = { **self.data,
                                  'auth_db': self.auth_db,
                                  'cb': self.cb }

    def on_post(self, req, resp):
        """
        Set the last heartbeat.
        ---
        summary: Status set.
        description: Set the last heartbeat.
        tags: [status]
        responses:
            200:
                description: Status data of the LCP.
                schema: StatusResponseSchema
            401:
                description: Unauthorized.
                schema: HTTPErrorSchema
        """
        data = req.context.get('json', {})
        id = data.get('id', None)
        self.data['id'] = id
        cb_expiration = data.get('cb_expiration', None)
        self.cb = {
            'password': data.get('cb_password', None),
            'expiration': cb_expiration,
            'host': req.host,
            'port': req.port
        }
        os.environ['CB_HOST'] = self.cb.get('host')
        os.environ['CB_PORT'] = str(self.cb.get('port'))
        username = data.get('username', None) # FIXME how to send username the first connection
        password = data.get('password', None)
        if username and self.auth_db.get(username, None) != utils.hash(password):
            raise falcon.HTTPUnauthorized({
                'title': '401 Unauthorized',
                'description': 'Invalid Username/Password'
            })
        if not username:
           username = utils.generate_username()
        password = utils.generate_password()
        self.auth_db[username] = utils.hash(password)
        # self.auth_db.set_ttl(username, (utils.str_to_datetime(cb_expiration) - datetime.now()).total_seconds()) # FIXME
        if id is not None:
            now = utils.datetime_to_str()
            self.data['last_hearthbeat'] = now
            if ArgReader.db.log_level == 'DEBUG':
                self.log.notice(f'Hearbeating from CB at {now} (password: {self.cb.get("password", None)} - expiration: {self.cb. get("expiration", None)})')
            else:
                self.log.notice(f'Hearbeating from CB at {now}')
        req.context['result'] = { **self.data,
                                  'username': username,
                                  'password': password }
