from argparse import ArgumentParser
from log import Log
from reader.config import ConfigReader
from utils.time import get_seconds


class ArgReader:
      db = None

      @classmethod
      def read(cls):
         cr = ConfigReader()

         ap = ArgumentParser(prog='python3 main.py', description=f'{cr.title}: {cr.description}')
         add = ap.add_argument

         add('--host', '-o', type=str, help='Hostname/IP of the REST Server', default=cr.lcp_host)
         add('--port', '-p', type=int, help='TCP Port of the REST Server', default=cr.lcp_port)

         add('--auth-max-ttl', '-t', type=str, help='Max authentication db TTL', default=cr.auth_max_ttl)

         add('--polycube-host', '-s', type=str, help='Hostname/IP of Polycube', default=cr.polycube_host)
         add('--polycube-port', '-c', type=int, help='Port of Polycube', default=cr.polycube_port)
         add('--polycube-timeout', '-w', type=str, help='Timeout for Polycube connection',
                                         default=cr.polycube_timeout)

         add('--dev-username', '-u', type=str, help='Authorized username', default=cr.dev_username)
         add('--dev-password', '-a', type=str, help='Authorized password', default=cr.dev_password)

         add('--log-level', '-l', choices=Log.get_levels(), help='Log level', default=cr.log_level)

         add('--write-config', '-w', help='Write options to config.ini', action='store_true')
         add('--version', '-v', help='Show version', action='store_const', const=cr.version)

         cls.db = ap.parse_args()
         cls.db.config = cr

         for field in ('auth_max_ttl',): setattr(cls.db, field, get_seconds(getattr(cls.db, field)))

         if cls.db.write_config: cr.write(cls.db)

         return cls.db
