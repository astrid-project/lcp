from configparser import BasicInterpolation as Basic_Interpolation
from configparser import ConfigParser as Config_Parser
from os import path
from pathlib import Path


class Config_Reader:
    path = Path(__file__).parent / '../config.ini'

    def __init__(self):
        self.cr = Config_Parser(interpolation=Config_Reader.Env_Interpolation())

    def read(self):
        self.cr.read(self.path.resolve())

        self.lcp_host = self.cr.get('local-control-plane', 'host', fallback='0.0.0.0')
        self.lcp_port = self.cr.get('local-control-plane', 'port', fallback=4000)
        self.lcp_https = self.cr.getboolean('local-control-plane', 'https', fallback=False)

        self.auth = self.cr.getboolean('auth', 'enabled', fallback=True)
        self.auth_header_prefix = self.cr.get('auth', 'header-prefix', fallback='ASTRID')
        self.auth_secret_key = self.cr.get('auth', 'secret-key', fallback='astrid-secret-key')

        self.elastic_apm_enabled = self.cr.getboolean('elastic-apm', 'enabled', fallback=False)
        self.elastic_apm_server = self.cr.get('elastic-apm', 'server', fallback='http://localhost:8200')

        self.polycube_host = self.cr.get('polycube', 'host', fallback='localhost')
        self.polycube_port = self.cr.get('polycube', 'port', fallback=9000)
        self.polycube_timeout = self.cr.get('polycube', 'timeout', fallback='20s')

        self.log_config = self.cr.get('log', 'config', fallback='log.yaml')

    def write(self, db):
        # FIXME is it necessary?
        self.cr.set('local-control-plane', 'port', db.port)

        with self.path.open('w') as f:
            self.cr.write(f)

    class Env_Interpolation(Basic_Interpolation):
        """Interpolation which expands environment variables in values."""

        def before_get(self, parser, section, option, value, defaults):
            """Execute before getting the value.

            :param self: class instance
            :param parser: configparser instance
            :param section: section value
            :param option: option value
            :param value: current value
            :param defaults: default values
            :returns: value with expanded variables
            """
            return path.expandvars(value)
