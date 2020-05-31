from marshmallow import Schema
from marshmallow.fields import Nested, String


class ConfigActionRequestSchema(Schema):
    """
    Action part in a single item of the code request.
    """
    cmd = String(required=True, description='Command.')
    args = String(many=True, description='Single command argument.', example='-al')


class ConfigParameterRequestSchema(Schema):
    """
    Parameter part in a single item of the code request.
    """
    scheme = String(required=True, description='Scheme.', choice=['json', 'yaml', 'ini'], example='yaml')
    source = String(required=True, description='Source filename.', example='filebeat.yml')
    path = String(required=True, many=True, description='Key path.', example='period')
    value = String(required=True, description='Parameter new value.', example='10s')


class ConfigResourceRequestSchema(Schema):
    """
    Resource part in a single item of the code request.
    """
    destination = String(required=True, description='Destination filename', example='filebeat.yml')
    content = String(required=True, description='Resource content.')


class ConfigRequestSchema(Schema):
    """
    Request for config endpoint.
    """
    actions = Nested(ConfigActionRequestSchema, many=True, description='List of actions.')
    parameters = Nested(ConfigParameterRequestSchema, many=True, description='List of parameters.')
    resources = Nested(ConfigResourceRequestSchema, many=True, description='List of resources.')

