from args import Args
from configparser import ConfigParser
from log import Log
from mode import Mode
from requests.auth import HTTPBasicAuth
from schema import *

import falcon
import hashlib
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

    routes = '/status',
    cb = {}
    auth_db = {}

    def __init__(self):
        """
        Set the data.
        """
        self.data = {
                'id': None,
                'started': utils.get_timestamp(),
                'last_hearthbeat': None
            }

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
        self.cb = {
            'password': data.get('cb_password', None),
            'expiration': data.get('cb_expiration', None)
        }
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
        StatusResource.auth_db[username] = utils.hash(password)
        if id is not None:
            now = utils.get_timestamp()
            self.data['last_hearthbeat'] = now
            log = Log.get('status')
            if Args.db.log_level == 'DEBUG':
                log.debug(f'Hearbeating from CB at {now} (password: {self.cb.get("password", None)} - expiration: {self.cb.get("expiration", None)})')
            else:
                log.info(f'Hearbeating from CB at {now}')
        req.context['result'] = { **self.data,
                                  'username': username,
                                  'password': password }
