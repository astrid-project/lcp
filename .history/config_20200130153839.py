# cspell:ignore unauth

from app import ns_config as ns
from setup import Setup
from flask_restplus import fields
from resource import Resource

class Config(BaseObject):
    LABEL = 'Config'


setup = Setup(target=Config, namespace=ns, model=None)


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
