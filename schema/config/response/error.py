from marshmallow import Schema
from marshmallow.fields import Boolean, String
from schema.config.response.result import ConfigResultResponseSchema


class ConfigErrorResponseSchema(ConfigResultResponseSchema):
    """
    Error related to a single item of config response.
    """
    error = Boolean(required=True, enum=[True], description='Indicate the presence of an error.', example=True)
    description = String(required=True, description='Human readable message that describes the error.',
                         example='Request type unknown')
