from configparser import BasicInterpolation as Basic_Interpolation, ConfigParser as Config_Parser
from os import path
from pathlib import Path
from utils.log import Log

__all__ = [
    'Config_Reader'
]


class Config_Reader:
    path = Path(__file__).parent / '../config.ini'

    def __init__(self):
        self.cr = Config_Parser(interpolation=Config_Reader.Env_Interpolation())

    def read(self):
        self.cr.read(self.path.resolve())

        self.lcp_host = self.cr.get('local-control-plane', 'host', fallback='0.0.0.0')
        self.lcp_port = self.cr.get('local-control-plane', 'port', fallback=4000)

        self.auth_max_ttl = self.cr.get('auth', 'max-ttl', fallback='10min')

        self.elastic_apm_server = self.cr.get('elastic-apm', 'server', fallback='http://localhost:8200');

        self.polycube_host = self.cr.get('polycube', 'host', fallback='localhost')
        self.polycube_port = self.cr.get('polycube', 'port', fallback=9000)
        self.polycube_timeout = self.cr.get('polycube', 'timeout', fallback='20s')

        self.dev_username = self.cr.get('dev', 'username', fallback='lcp')
        self.dev_password = self.cr.get('dev', 'password', fallback='9c804f2550e31d8f98ac9b460cfe7fbfc676c5e4452a261a2899a1ea168c0a50') # astrid in sha256

        self.log_level = self.cr.get('log', 'level', fallback='INFO')

        Log.init(default=self.log_level, levels=self.cr.items('log') if self.cr.has_section('log') else [])

    def write(self, db):
        self.cr.set('local-control-plane', 'port', db.port)
        self.cr.set('context-broker', 'endpoint', db.cb_endpoint)

        with self.path.open('w') as f:
            self.cr.write(f)

    class Env_Interpolation(Basic_Interpolation):
        """Interpolation which expands environment variables in values."""

        def before_get(self, parser, section, option, value, defaults):
            """Executes before getting the value.

            :param self: class instance
            :param parser: configparser instance
            :param section: section value
            :param option: option value
            :param value: current value
            :param defaults: default values
            :returns: value with expanded variables
            """
            return path.expandvars(value)
