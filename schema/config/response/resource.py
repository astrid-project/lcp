from marshmallow import Schema
from marshmallow.fields import String
from schema.config.response.result import ConfigResultResponseSchema


class ConfigResourceResponseSchema(ConfigResultResponseSchema):
    """
    Resource part in a single item of the config response.
    """
    destination = String(required=True, description='Destination filename', example='filebeat.yml')
