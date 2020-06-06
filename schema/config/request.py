from marshmallow import Schema
from marshmallow.fields import Nested, Str


class ConfigActionRequestSchema(Schema):
    """Action part in a single item of the code request."""
    cmd = Str(required=True, description='Command.')
    args = Str(many=True, description='Single command argument.', example='-al')
    daemon = Str(description='Key used to execute the command as daemon.', example='firewall')


class ConfigParameterRequestSchema(Schema):
    """Parameter part in a single item of the code request."""
    scheme = Str(required=True, description='Scheme.', choice=['json', 'yaml', 'ini'], example='yaml')
    source = Str(required=True, description='Source filename.', example='filebeat.yml')
    path = Str(required=True, many=True, description='Key path.', example='period')
    value = Str(required=True, description='Parameter new value.', example='10s')


class ConfigResourceRequestSchema(Schema):
    """Resource part in a single item of the code request."""
    path = Str(required=True, description='File path', example='filebeat.yml')
    content = Str(required=True, description='Resource content.')


class ConfigRequestSchema(Schema):
    """Request for config endpoint."""
    actions = Nested(ConfigActionRequestSchema, many=True, description='List of actions.')
    parameters = Nested(ConfigParameterRequestSchema, many=True, description='List of parameters.')
    resources = Nested(ConfigResourceRequestSchema, many=True, description='List of resources.')
