from marshmallow import Schema
from marshmallow.fields import String


class CodeResultResponseSchema(Schema):
    """
    Single item of the code results.
    """
    warning = String(description='Warning message.', example='Useless properties: id')
