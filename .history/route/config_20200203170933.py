from datetime import datetime
import falcon
from marshmallow import fields, Schema
import subprocess

class ConfigRequestSchema(Schema):
    pass


class ConfigResponseSchema(Schema):
    pass


class ConfigResource(object):
    request_schema = ConfigRequestSchema()
    response_schema = ConfigResponseSchema()

    pass
