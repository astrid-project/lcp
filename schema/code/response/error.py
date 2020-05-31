from marshmallow import Schema
from marshmallow.fields import Constant, String
from schema.code.response.result import CodeResultResponseSchema


class CodeErrorResponseSchema(CodeResultResponseSchema):
    """
    Error related to a single item of code response.
    """
    error = Constant(required=True, constant=True, description='Indicate the presence of an error.')

    description = String(required=True, description='Human readable message that describes the error.',
                         example='Missing name.')
