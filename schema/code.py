from marshmallow.fields import Str

from schema.base import Base_Schema
from utils.schema import List_or_One


# FIXME add missing required fields
class Code_Request_Schema(Base_Schema):
    """Request for code endpoint."""

    id = Str(required=True, example='firewall', description='Code id.')
    code = List_or_One(Str, required=True, description='Code source')
