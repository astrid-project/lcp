from marshmallow import Schema
from marshmallow.fields import String
from schema.code.response.result import CodeResultResponseSchema


class CodeInjectedResponseSchema(CodeResultResponseSchema):
    """
    Single item of the code inject response.
    """
    name = String(required=True, description='Code name', example='firewall')
    injected = Boolean(required=True, description='Indicate if the code was injected.', example=True)
