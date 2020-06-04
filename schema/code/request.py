from marshmallow import Schema
from marshmallow.fields import Str


class CodeRequestSchema(Schema):
    """Request for code endpoint."""
    name = Str(required=True, description='Code name.', example='firewall')
    source = Str(required=True, description='Code source')
