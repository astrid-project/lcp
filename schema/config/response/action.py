from marshmallow import Schema
from marshmallow.fields import Integer, String
from schema.config.response.result import ConfigResultResponseSchema


class ConfigActionResponseSchema(ConfigResultResponseSchema):
    """
    Action part in a single item of the config response.
    """
    execute = String(required=True, description='Command executed.', example='ls -al')
    stdout = String(description='Standard output of the execution.')
    stderr = String(description='Standard error output of the execution.')
    return_code = Integer(data_key='return-code', required=True,
                          description='Exit code of the execution (0: no error).', example=0)
