from flask import Flask
from flask_restplus import Api, Namespace
import logging

title = 'ASTRID Local Control Plane (LCP)'

app = Flask(title)
app.config['ERROR_404_HELP'] = False

log = logging.getLogger('ASTRID')
log.setLevel(logging.DEBUG)

ns_code = Namespace('code', path='/code', description='Code@runtime')
ns_config = Namespace('config', path='/config', description='Configuration@runtime')

api = Api(app,
          catch_all_404s=True,
          version='0.0.1',
          title=title,
          description='Programmability of local agent changing the behavior of the data plane at run-time.')
#   terms_url = 'TODO',
#   contact = 'TODO',
#   license =  'TODO',
#   license_url = 'TODO',
#   endpoint = 'TODO',
#   default = 'TODO',
#   default_label =  'TODO',
#   validate = True,
#   ordered = True,
#   doc = 'TODO',
#   catch_all_404s = True,
#   authorizations = [],
#   serve_challenge_on_401 = True,
#   format_checker = False)

api.add_namespace(ns_code)
api.add_namespace(ns_config)
