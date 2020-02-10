# cspell:ignore unauth

from app import ns_config as ns
from config import Config
from flask_restplus import fields
from resource import Resource

cnf = Config(target=ref, namespace=ns, model=None)


@cnf.route
@cnf.unauth
@cnf.forbidden
@cnf.headers
class Base(Resource):
    @cnf.doc
    @cnf.input
    @cnf.accepted
    @cnf.not_found
    def delete(self):
        return ref.deleted()

    @cnf.doc
    @cnf.input
    @cnf.ok
    @cnf.not_found
    def get(self):
        return ref.read()

    @cnf.doc
    @cnf.input
    @cnf.created
    @cnf.conflict
    def post(self):
        return ref.created()


@cnf.route_selected
@cnf.unauth
@cnf.forbidden
@cnf.headers
class Selected(Resource):
    @cnf.doc
    @cnf.input
    @cnf.not_found
    def put(self, id):
        return ref.updated(id)
