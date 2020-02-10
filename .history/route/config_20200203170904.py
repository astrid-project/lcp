from datetime import datetime
import falcon
from marshmallow import fields, Schema
import subprocess

class CmdRequestSchema(Schema):
    prog = fields.String()
    args = fields.List(fields.String())


class ConfigRequestSchema(Schema):
    pass

class ConfigResponseSchema(Schema):
    pass

class ConfigResource(object):
        request_schema = CodeRequestSchema()
    response_schema = CodeResponseSchema()

    pass
