# cspell:ignore unauth

from app import api
from setup import Setup
from flask_restplus import fields
from resource import Resource

class Config(BaseObject):
    LABEL = 'Config'

model = ns.model(ref.Index.name, {
    'id':  fields.String(description='Unique ID', required=True, example='exec-env-apache'),
    'hostname': fields.String(description=f'Hostname where the {ref.LABEL} is allocated', required=True, example='host.domain.com'),
    'type_id': fields.String(description=f'{ExecEnvType.LABEL} ID', required=True, example='vm')
}, description=f'{ref.LABEL} object', additionalProperties=True)

setup = Setup(target=Config, api=api, model=model)


@setup.route
@setup.unauth
@setup.forbidden
@setup.headers
class Base(Resource):
    @setup.doc
    @setup.input
    @setup.accepted
    @setup.not_found
    def delete(self):
        return ref.deleted()

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
        return ref.created()


@setup.route_selected
@setup.unauth
@setup.forbidden
@setup.headers
class Selected(Resource):
    @setup.doc
    @setup.input
    @setup.not_found
    def put(self, id):
        return ref.updated(id)
