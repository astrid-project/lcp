from datetime import datetime
import falcon
from marshmallow import fields, Schema
import subprocess

class CmdRequestSchema(Schema):
    prog = fields.String()
    args = fields.List(fields.String())


class CodeRequestSchema(Schema):
    cmds = fields.List(fields.Nested(CmdRequestSchema()))


class CmdResponseScheme(Schema):
    when = fields.DateTime()
    cmd = fields.String()
    args: fields.List(fields.String())
    stdout: fields.String()
    stderr: fields.String()
    return_code: fields.Integer()


class ConfigResponseSchema(Schema):
    when = fields.DateTime()
    cmds = fields.List(fields.Nested(CmdResponseScheme()))
    return_code = fields.Integer()


class ConfigResource(object):

    pass
