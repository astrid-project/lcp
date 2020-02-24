from http import HTTPStatus
from marshmallow import fields, Schema


class HTTPErrorSchema(Schema):
    """
    HTTP Error Schema.
    """
    title = fields.String(required=True, description='Title error',
                          example='400 Bad Request')
    description = fields.String(required=True, description='Human readable message that describes the error.',
                                example='Could not decode the request body, either because it was not valid JSON or because it was not encoded as UTF-8.')
