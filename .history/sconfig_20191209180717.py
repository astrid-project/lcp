from app import ns_config as ns
from config import Config
from document import Document, InnerDoc
from elasticsearch_dsl import Text, Boolean, Nested
from flask_restplus import fields
from resource import Resource

type_values = ['integer', 'number', 'time-duration',
               'string', 'choice', 'obj', 'boolean', 'binary']


def type_check(data):
    return not data['type'] in ['choice', 'obj'] or 'value' in data


class AgentParameter(InnerDoc):
    LABEL = 'Agent Parameter'

    name = Text()
    type = Text()
    list = Boolean()

    class Index:
        name = 'agent-parameter'

    @staticmethod
    def apply(data):
        if 'list' not in data:
            data['list'] = False


ref = AgentParameter

agent_parameter_model = ns.model(ref.Index.name, {
    'name': fields.String(description='Name', required=True, example='polling'),
    'type': fields.String(description='Parameter type', required=True, enum=type_values, example='time-duration')
}, description='Represent the available parameters for each agent in the catalog', additionalProperties=True)

type_values = ['filename']


class AgentCatalog(Document):
    LABEL = 'Agent in Catalog'

    name = Text()
    parameters = Nested(AgentParameter)

    class Index:
        name = 'agent-catalog'

    @staticmethod
    def get_url():
        return 'agent'


ref = AgentCatalog

model = ns.model(ref.Index.name, {
    'id':  fields.String(description='Unique ID', required=True, example='filebeat'),
    'name': fields.String(description='General name', required=True, example='Filebeat'),
    'parameters': fields.List(fields.Nested(agent_parameter_model), description='List of parameters', required=False),
}, description='Represent the available agent in the catalog', additionalProperties=True)

cnf = Config(target=ref, namespace=ns, model=model)


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
