from datetime import datetime
import falcon
from marshmallow import fields, Schema
import subprocess

class CmdRequestSchema(Schema):
    prog = fields.String()
    args = fields.List(fields.String())


class CodeRequestSchema(Schema):
    cmds = fields.List(fields.Nested(CmdRequestSchema()))



class ConfigResponseSchema(Schema):
    when = fields.DateTime()
    return_code = fields.Integer()


class ConfigResource(object):

    pass
