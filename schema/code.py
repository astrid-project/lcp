from marshmallow.fields import Bool, DateTime as Date_Time, Nested, Str
from schema.base import Base_Schema
from utils.datetime import FORMAT

__all__ = [
    'Code_Request_Schema'
]


class Code_Request_Schema(Base_Schema):
    """Request for code endpoint."""

    name = Str(required=True, example='firewall',
               description='Code name.')
    source = Str(required=True,
                 description='Code source')
