from http import HTTPStatus
from marshmallow import Schema
from marshmallow.fields import Str


class HTTPErrorSchema(Schema):
    """HTTP Error Schema."""
    title = Str(required=True, description='Title error',
                example='400 Bad Request')
    description = Str(required=True, description='Human readable message that describes the error.',
                      example='The request body is not a valid JSON or it is not encoded as UTF-8.')
