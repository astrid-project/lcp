from marshmallow import Schema
from marshmallow.fields import String


class ConfigResourceRequestSchema(Schema):
    """
    Resource part in a single item of the code request.
    """
    destination = String(required=True, description='Destination filename', example='filebeat.yml')
    content = String(required=True, description='Resource content.')
