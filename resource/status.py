# cspell:ignore strftime

from configparser import ConfigParser
from datetime import datetime
from mode import Mode
from requests.auth import HTTPBasicAuth
from schema import StatusResponseSchema
import atexit
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
        Set the data and register the LCP to the context broker (if mode is slave).
        """
        self.args = args
        self.num_attempts = 0
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
        """
        Update the status of the LCP to the context broker (if mode is slave).
        """
        if self.args.mode == Mode.slave:
            print('Info: update the register data in the context-broker.')
            self.num_attempts = 0
            self.data['started'] = False
            self.cb_connection()

    def cb_connection(self):
        """
        Register the LCP to the context broker (if mode is slave).
        Try periodically if the context broker does not respond.
        """
        self.num_attempts += 1
        print(f'Info: connecting #{self.num_attempts} to context-broker ({self.args.cb_endpoint}) with timeout: {self.args.cb_timeout}.')
        try:
            res = requests.put(f'http://{self.args.cb_endpoint}/config/exec-env',
                                auth=HTTPBasicAuth(self.args.cb_username, self.args.cb_password),
                                timeout=self.args.cb_timeout,
                                json={'id': self.args.id, 'started': self.data['started']})
        except:
            print(f'Error: connection to context-broker ({self.args.cb_endpoint}) failed.')
            self.data['connected-to-cb'] = False
        else:
            try:
                res_data = res.json()
                if res_data[0]['status'] in ['updated', 'noop']:
                    print(f'Success: connected to context-broker ({self.args.cb_endpoint}).')
                    self.data['connected-to-cb'] = True
                else:
                    print(f'Error: registration to context-broker ({self.args.cb_endpoint}) not possible.')
                    self.data['connected-to-cb'] = False
            except:
                print(f'Error: response from to context-broker ({self.args.cb_endpoint}) unknown.')
                self.data['connected-to-cb'] = False
        if not self.data['connected-to-cb']:
            print(f'Info: retry connection to context-broker between {self.args.cb_retry_every_seconds} seconds.')
            threading.Timer(self.args.cb_retry_every_seconds, self.cb_connection).start()

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
