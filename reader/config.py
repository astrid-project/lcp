from configparser import ConfigParser
from log import Log
from utils import EnvInterpolation

import git


class ConfigReader:
   def __init__(self):
      self.cr = ConfigParser(interpolation=EnvInterpolation())
      repo = git.Repo(search_parent_directories=True)
      self.version = f'{repo.head.object.hexsha}@{repo.active_branch}'

   def read(self):
      self.cr.read('config.ini')

      self.title = self.cr.get('info', 'title')
      self.description = self.cr.get('info', 'description')

      self.lcp_host = self.cr.get('local-control-plane', 'host')
      self.lcp_port = self.cr.get('local-control-plane', 'port')

      self.auth_max_ttl = self.cr.get('auth', 'max-ttl')

      self.dev_username = self.cr.get('dev', 'username')
      self.dev_password = self.cr.get('dev', 'password')

      self.log_level = self.cr.get('log', 'level')

      Log.init(default=self.log_level, levels=self.cr.items('log'))


   def write(self, db):
      self.cr.set('local-control-plane', 'port', db.port)
      self.cr.set('context-broker', 'endpoint', db.cb_endpoint)

      with open('config.ini', 'w') as f:
         self.cr.write(f)
