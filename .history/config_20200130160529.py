# cspell:ignore unauth

from app import api
from document import Document
from setup import Setup
from flask_restplus import fields
from resource import Resource

action_values = ['start', 'stop', 'update']

class Config(Document):
    LABEL = 'Config'

ref = Config

model = ns.model(ref.LABEL, {
    'id':  fields.String(description='Unique ID of the agent', required=True, example='filebeat-1'),
    'action': fields.String(description=f'Action to execute for the specific agent', required=True, example='start', enum=action_values),
    'command': fields.String(description=f'Command for the specified action', required=True, example='filebeat')
}, description=f'{ref.LABEL} object', additionalProperties=True)

setup = Setup(target=Config, namespace=api, model=model)


@setup.route
@setup.unauth
@setup.forbidden
@setup.headers
class ConfigBase(Resource):
    @setup.doc
    @setup.input
    @setup.ok
    @setup.not_found
    def get(self):
        return ref.read()

    @setup.doc
    @setup.input
    @setup.created
    @setup.conflict
    def post(self):
        return ref.executed()


@setup.route_selected
@setup.unauth
@setup.forbidden
@setup.headers
class ConfigSelected(Resource):
    @setup.doc
    @setup.input
    @setup.not_found
    def put(self, id):
        return ref.updated(id)
