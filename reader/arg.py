from argparse import ArgumentParser as Argument_Parser

from about import description, title, version
from reader.config import Config_Reader
from utils.time import get_seconds


class Arg_Reader:
    db = None
    cr = None
    ap = None

    @classmethod
    def init(cls):
        cls.cr = Config_Reader()
        cls.cr.read()
        cls.ap = Argument_Parser(prog='python3 main.py',
                                 description=f'{title}: {description}')
        add = cls.ap.add_argument

        add('--host', '-o', type=str, help='Hostname/IP of the REST Server', default=cls.cr.lcp_host)
        add('--port', '-p', type=int, help='TCP Port of the REST Server', default=cls.cr.lcp_port)
        add('--https', '-q', help='Force to use HTTPS instead of HTTP', action='store_true')

        add('--auth', '-t', help='Enable JWT authentication', action='store_true')
        add('--auth-header-prefix', '-x', type=str, help='Prefix in the JWT authentication header', default=cls.cr.auth_header_prefix)
        add('--auth-secret-key', '-k', type=str, help='Secret key for JWT authentication', default=cls.cr.auth_secret_key)

        add('--polycube-host', '-s', type=str, help='Hostname/IP of Polycube', default=cls.cr.polycube_host)
        add('--polycube-port', '-c', type=int, help='Port of Polycube', default=cls.cr.polycube_port)
        add('--polycube-timeout', '-e', type=str, help='Timeout for Polycube connection', default=cls.cr.polycube_timeout)

        add('--apm-enabled', '-n', help='Enable Elastic APM integration', action='store_true')
        add('--apm-server', '-m', type=str, help='Elastic APM hostname/IP:port', default=cls.cr.elastic_apm_server)

        add('--log-config', '-l', help='Path of the log configuration file (e.g. log.yaml)', default=cls.cr.log_config)

        add('--write-config', '-w', help='Write options to config.ini', action='store_true')
        add('--version', '-v', help='Show version', action='store_const', const=version)

        return cls.ap

    @classmethod
    def read(cls):
        cls.init()

        cls.db = cls.ap.parse_args()
        cls.db.config = cls.cr
        for field in ['polycube_timeout']:
            setattr(cls.db, field, get_seconds(getattr(cls.db, field)))

        if cls.db.write_config:
            cls.cr.write(cls.db)

        return cls.db
