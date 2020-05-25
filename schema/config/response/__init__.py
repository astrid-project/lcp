from marshmallow import Schema
from marshmallow.fields import DateTime, Nested
from schema.config.response.result import ConfigResultResponseSchema


class ConfigResponseSchema(Schema):
    """
    Response for config endpoint.
    """
    when = DateTime(required=True, description='Datetime of the configuration changes',
                           example='2020/02/13 15:27:06')
    results = Nested(ConfigResultResponseSchema, many=True, required=True)
