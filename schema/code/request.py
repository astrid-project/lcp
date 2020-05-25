from marshmallow import Schema
from marshmallow.fields import String


class CodeRequestSchema(Schema):
    """
    Request for code endpoint.
    """
    name = String(required=True, description='Code name.', example='firewall')
    source = String(required=True, description='Code source')
