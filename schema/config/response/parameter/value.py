from marshmallow import Schema
from marshmallow.fields import String


class ConfigParameterValueResponseSchema(Schema):
    """
    Parameter value part in a single item of the config response.
    """
    new = String(required=True, description='New value.', example='5s')
    old = String(required=True, description='Old value', example='10s')

