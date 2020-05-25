from marshmallow import Schema
from marshmallow.fields import String


class ConfigResultResponseSchema(Schema):
    """
    Single item of the config response.
    """
    type = String(required=True, description='Configuration type.')
    warning = String(description='Warning message', example='Useless property: id')
