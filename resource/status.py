# cspell:ignore strftime

from .base import BaseResource
from configparser import ConfigParser
from datetime import datetime
from mode import Mode
from requests.auth import HTTPBasicAuth
from schema import StatusResponseSchema
import atexit
import falcon
import requests
import threading


class StatusResource(BaseResource):
    request_schema = None
    response_schema = StatusResponseSchema()

    routes = '/status',

    def __init__(self, config_parser, args):
        atexit.register(self.exit_handler)
        self.num_attempts = 0
        self.args = args
        self.data = {
                'id': args.id,
                'mode': args.mode,
                'agents': [],
                'started': datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
            }
        if args.mode == Mode.master:
            pass
        elif args.mode == Mode.slave:
            if args.id is None:
                self.data['error'] = True
                self.data['description'] = 'ID not provided'
            else:
                self.cb_connection()

    def exit_handler(self):
        print('Update the register in the context-broker')
        self.num_attempts = 0
        self.data['started'] = False
        self.cb_connection()

    def cb_connection(self):
        self.num_attempts += 1
        print(f'Connecting #{self.num_attempts} to context-broker ({self.args.cb_endpoint}) with timeout: {self.args.cb_timeout}')
        try:
            res = requests.put(f'http://{self.args.cb_endpoint}/config/exec-env',
                                auth=HTTPBasicAuth(self.args.cb_username, self.args.cb_password),
                                timeout=self.args.cb_timeout,
                                json={'id': self.args.id, 'started': self.data['started']})
        except requests.exceptions.ConnectionError:
            print(f'Error: connection to context-broker ({self.args.cb_endpoint}) failed')
            self.data['connected-to-cb'] = False
        else:
            try:
                res_data = res.json()
                if res_data[0]['status'] in ['updated', 'noop']:
                    print(f'Connected to context-broker ({self.args.cb_endpoint})')
                    self.data['connected-to-cb'] = True
                else:
                    print(f'Error: registration to context-broker ({self.args.cb_endpoint}) not possible')
                    self.data['connected-to-cb'] = False
            except:
                print(f'Error: response from to context-broker ({self.args.cb_endpoint}) unknown')
                self.data['connected-to-cb'] = False
        if not self.data['connected-to-cb']:
            threading.Timer(self.args.cb_retry_every_seconds, self.cb_open_connection).start()

    def on_get(self, req, resp):
        """
        Get info about the status of the LCP in the execution environment.
        ---
        summary: Configuration update
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
