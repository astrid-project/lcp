from about import title, description, version
from argparse import ArgumentParser as Argument_Parser
from reader.config import Config_Reader
from utils.log import Log
from utils.time import get_seconds

__all__ = [
    'Arg_Reader'
]


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


        add('--host', '-o', type=str,
            help='Hostname/IP of the REST Server', default=cls.cr.lcp_host)
        add('--port', '-p', type=int,
            help='TCP Port of the REST Server', default=cls.cr.lcp_port)

        add('--auth-max-ttl', '-t', type=str,
            help='Max authentication db TTL', default=cls.cr.auth_max_ttl)

        add('--polycube-host', '-s', type=str,
            help='Hostname/IP of Polycube', default=cls.cr.polycube_host)
        add('--polycube-port', '-c', type=int,
            help='Port of Polycube', default=cls.cr.polycube_port)
        add('--polycube-timeout', '-e', type=str, help='Timeout for Polycube connection',
            default=cls.cr.polycube_timeout)

        add('--apm-server', '-m', type=str,
            help='Elastic APM hostname/IP:port',
            default=cls.cr.elastic_apm_server)

        add('--dev-username', '-u', type=str,
            help='Authorized username', default=cls.cr.dev_username)
        add('--dev-password', '-a', type=str,
            help='Authorized password', default=cls.cr.dev_password)

        add('--log-level', '-l', choices=Log.get_levels(),
            help='Log level', default=cls.cr.log_level)

        add('--write-config', '-w',
            help='Write options to config.ini', action='store_true')
        add('--version', '-v', help='Show version',
            action='store_const', const=version)
        return cls.ap

    @classmethod
    def read(cls):
        cls.init()

        cls.db = cls.ap.parse_args()
        cls.db.config = cls.cr
        for field in ('auth_max_ttl', 'polycube_timeout'):
            setattr(cls.db, field, get_seconds(getattr(cls.db, field)))

        if cls.db.write_config:
            cls.cr.write(cls.db)

        return cls.db
