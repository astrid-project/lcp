from configparser import ConfigParser
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
    cb_password = None
    auth_db = {}

    def __init__(self, args):
        """
        Save the program arguments.
        Set the data.
        """
        self.args = args
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
        req.context['result'] = self.data

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
        StatusResource.cb_password = data.get('cb_password', None)
        username = data.get('username', None) # FIXME how to send username the first connection
        if username:
            del StatusResource.auth_db[username]
        username = utils.generate_username()
        password = utils.generate_password()
        StatusResource.auth_db[username] = utils.hash(password)
        if id is not None:
            now = utils.get_timestamp()
            self.data['last_hearthbeat'] = now
            if self.args.dev_debug:
                print(f'Hearbeating from CB at {now} (password: {StatusResource.cb_password})')
            else:
                print(f'Hearbeating from CB at {now}')
        req.context['result'] = { **self.data,
                                  'username': username,
                                  'password': password }
