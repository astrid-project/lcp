from marshmallow import Schema
from marshmallow.fields import Boolean, String
from schema.code.response.result import CodeResultResponseSchema


class CodeErrorResponseSchema(CodeResultResponseSchema):
    """
    Error related to a single item of code response.
    """
    error = Boolean(required=True, enum=[True], description='Indicate the presence of an error.', example=True)
    description = String(required=True, description='Human readable message that describes the error.',
                         example='Missing name')
