from marshmallow import Schema
from marshmallow.fields import Constant, DateTime, Integer, Nested, String


class ConfigResultResponseSchema(Schema):
    """
    Single item of the config response.
    """
    type = String(required=True, description='Configuration type.')
    warning = String(description='Warning message', example='Useless property: id')


class ConfigActionResponseSchema(ConfigResultResponseSchema):
    """
    Action part in a single item of the config response.
    """
    execute = String(required=True, description='Command executed.', example='ls -al')
    stdout = String(description='Standard output of the execution.')
    stderr = String(description='Standard error output of the execution.')
    return_code = Integer(data_key='return-code', required=True,
                          description='Exit code of the execution (0: no error).', example=0)


class ConfigErrorResponseSchema(ConfigResultResponseSchema):
    """
    Error related to a single item of config response.
    """
    error = Constant(required=True, constant=True, description='Indicate the presence of an error.')
    description = String(required=True, description='Human readable message that describes the error.',
                         example='Request type unknown')


class ConfigResourceResponseSchema(ConfigResultResponseSchema):
    """
    Resource part in a single item of the config response.
    """
    destination = String(required=True, description='Destination filename', example='filebeat.yml')


class ConfigResponseSchema(Schema):
    """
    Response for config endpoint.
    """
    when = DateTime(required=True, description='Datetime of the configuration changes',
                    example='2020/02/13 15:27:06')
    results = Nested(ConfigResultResponseSchema, many=True, required=True)
