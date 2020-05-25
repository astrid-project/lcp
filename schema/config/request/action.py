from marshmallow import Schema
from marshmallow.fields import List, String


class ConfigActionRequestSchema(Schema):
    """
    Action part in a single item of the code request.
    """
    cmd = String(required=True, description='Command.')
    args = List(String(description='Single command argument.', example='-al'), description='Command arguments.')
