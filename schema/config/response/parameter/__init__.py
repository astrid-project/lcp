from marshmallow import Schema
from marshmallow.fields import List, Nested, String
from schema.config.response.result import ConfigResultResponseSchema
from schema.config.response.parameter.value import ConfigParameterValueResponseSchema


class ConfigParameterResponseSchema(ConfigResultResponseSchema):
    """
    Parameter part in a single item of the config response.
    """
    scheme = String(required=True, description='Scheme.', choice=['json', 'yaml', 'ini'], example='yaml')
    source = String(required=True, description='Source filename.', example='filebeat.yml')
    path = List(String(required=True, description='Path item.', example='period'), description='Key path')
    # TODO It is when note is present.
    value = Nested(ConfigParameterValueResponseSchema, many=False, required=True)
    note = String(required=False, description='Additional note', example='No change ne')

