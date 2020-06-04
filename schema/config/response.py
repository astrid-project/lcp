from marshmallow import Schema
from marshmallow.fields import Constant, DateTime, Integer, List, Nested, Str


class ConfigResultResponseSchema(Schema):
    """Single item of the config response."""
    type = Str(required=True, description='Configuration type.')
    warning = Str(description='Warning message',
                  example='Useless property: id')


class ConfigActionResponseSchema(ConfigResultResponseSchema):
    """Action part in a single item of the config response."""
    execute = Str(required=True, description='Command executed.',
                  example='ls -al')
    stdout = Str(description='Standard output of the execution.')
    stderr = Str(description='Standard error output of the execution.')
    return_code = Integer(data_key='return-code', required=True,
                          description='Exit code of the execution (0: no error).', example=0)


class ConfigParameterValueResponseSchema(Schema):
    """Parameter value part in a single item of the config response."""
    new = Str(required=True, description='New value.', example='5s')
    old = Str(required=True, description='Old value', example='10s')


class ConfigParameterResponseSchema(ConfigResultResponseSchema):
    """Parameter part in a single item of the config response."""
    scheme = Str(required=True, description='Scheme.', example='yaml',
                 choice=['json', 'yaml', 'ini'])
    source = Str(required=True, description='Source filename.',
                 example='filebeat.yml')
    path = List(Str(required=True, description='Path item.',
                    example='period'), description='Key path')
    value = Nested(ConfigParameterValueResponseSchema,
                   many=False, required=True)
    note = Str(required=False, description='Additional note.',
               example='No change needed.')


class ConfigResourceResponseSchema(ConfigResultResponseSchema):
    """Resource part in a single item of the config response."""
    destination = Str(required=True, example='filebeat.yml',
                      description='Destination filename')


class ConfigErrorResponseSchema(ConfigResultResponseSchema):
    """Error related to a single item of config response."""
    error = Constant(required=True, constant=True,
                     description='Indicate the presence of an error.')
    description = Str(required=True, description='Human readable message that describes the error.',
                      example='Request type unknown')


class ConfigResponseSchema(Schema):
    """Response for config endpoint."""
    when = DateTime(required=True, description='Datetime of the configuration changes',
                    example='2020/02/13 15:27:06')
    results = Nested(ConfigResultResponseSchema, many=True, required=True)
