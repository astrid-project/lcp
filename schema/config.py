from marshmallow import Schema, validate
from marshmallow.fields import Boolean, Constant, DateTime, Integer, List, Nested, Raw, Str
from utils.datetime import FORMAT


parameter_schemas = ['json', 'yaml', 'properties']


class ConfigActionRequestSchema(Schema):
    """Action part in a single item of the code request."""
    cmd = Str(required=True,
              description='Command.')
    args = Str(many=True, example='-al',
               description='Single command argument.')
    daemon = Str(example='firewall',
                 description='Key used to execute the command as daemon.')


class ConfigParameterRequestSchema(Schema):
    """Parameter part in a single item of the code request."""
    schema = Str(required=True, enum=parameter_schemas, example='yaml',
                 description='Scheme.',
                 validate=validate.OneOf(parameter_schemas))
    source = Str(required=True, example='filebeat.yml',
                 description='Source filename.')
    path = List(Str(required=True, example='period',
                    description='Key path.'))
    value = Str(required=True, example='10s',
                description='Parameter new value.')


class ConfigResourceRequestSchema(Schema):
    """Resource part in a single item of the code request."""
    path = Str(required=True, example='filebeat.yml',
               description='File path')
    content = Str(required=True,
                  description='Resource content.')


class ConfigRequestSchema(Schema):
    """Request for config endpoint."""
    actions = Nested(ConfigActionRequestSchema, many=True,
                     description='List of actions.')
    parameters = Nested(ConfigParameterRequestSchema, many=True,
                        description='List of parameters.')
    resources = Nested(ConfigResourceRequestSchema, many=True,
                       description='List of resources.')


class ConfigBaseResponseSchema(Schema):
    """Single item of the config response."""
    type = Str(required=True,
               description='Configuration type.')
    warning = Str(description='Warning message',
                  example='Useless property: id')


class ConfigActionResponseSchema(ConfigBaseResponseSchema):
    """Action part in a single item of the config response."""
    error = Boolean(default=False, example=True,
                    description='Indicate the presence of an error.')
    executed = Str(required=True, example='ls -al',
                   description='Command executed.')
    stdout = Raw(many=True,
                 description='Standard output of the execution.')
    stderr = Raw(many=True,
                 description='Standard error output of the execution.')
    daemon = Str(example='firewall',
                 description='Key used to execute the command as daemon.')
    return_code = Integer(required=True, example=0,
                          description='Exit code of the execution (0: no error).')


class ConfigParameterValueResponseSchema(Schema):
    """Parameter value part in a single item of the config response."""
    new = Str(required=True, example='5s',
              description='New value.')
    old = Str(required=True, example='10s',
              description='Old value')


class ConfigParameterResponseSchema(ConfigBaseResponseSchema):
    """Parameter part in a single item of the config response."""
    schema = Str(required=True, example='yaml', enum=parameter_schemas,
                 description='Scheme.',
                 validate=validate.OneOf(parameter_schemas))
    source = Str(required=True, example='filebeat.yml',
                 description='Source filename.')
    path = Str(required=True, many=True, example='period',
               description='Key path')
    value = Nested(ConfigParameterValueResponseSchema,
                   required=True)
    note = Str(required=False, example='No change needed.',
               description='Additional note.')


class ConfigResourceResponseSchema(Schema):
    """Resource part in a single item of the config response."""
    path = Str(required=True, example='filebeat.yml',
               description='File path')


class ConfigErrorResponseSchema(ConfigBaseResponseSchema):
    """Error related to a single item of config response."""
    error = Constant(required=True, constant=True,
                     description='Indicate the presence of an error.')
    description = Str(required=True, example='Request type unknown',
                      description='Human readable message that describes the error.')


class ConfigResultResponseSchema(Schema):  # TODO
    pass


class ConfigResponseSchema(Schema):
    """Response for config endpoint."""
    when = DateTime(format=FORMAT, required=True, example='2020/02/13 15:27:06',
                    description='Datetime of the configuration changes',)
    results = Nested(ConfigResultResponseSchema, many=True, required=True)
