from marshmallow import Schema
from marshmallow.fields import Nested
from schema.config.request.action import ConfigActionRequestSchema
from schema.config.request.parameter import ConfigParameterRequestSchema
from schema.config.request.resource import ConfigResourceRequestSchema


class ConfigRequestSchema(Schema):
    """
    Request for config endpoint.
    """
    actions = Nested(ConfigActionRequestSchema, many=True, description='List of actions.')
    parameters = Nested(ConfigParameterRequestSchema, many=True, description='List of parameters.')
    resources = Nested(ConfigResourceRequestSchema, many=True, description='List of resources.')

