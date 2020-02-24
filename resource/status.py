# cspell:ignore strftime

from configparser import ConfigParser
from datetime import datetime
from mode import Mode
from requests.auth import HTTPBasicAuth
from schema import StatusResponseSchema
import falcon
import requests
import threading


class StatusResource(object):
    request_schema = None
    response_schema = StatusResponseSchema()

    routes = '/status',

    def __init__(self, args):
        """
        Save the program arguments.
        Set the data.
        """
        self.args = args
        self.data = {
                'id': None,
                'started': self.get_timestamp(),
                'last_hearthbeat': None
            }

    def get_timestamp(self):
        return datetime.now().strftime("%Y/%m/%d-%H:%M:%S")

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
                schema: UnauthorizedSchema
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
                schema: UnauthorizedSchema
        """
        data = req.context.get('json', {})
        id = data.get('id', None)
        self.data['id'] = id
        if id is not None:
            self.data['last_hearthbeat'] = self.get_timestamp()
        req.context['result'] = self.data
