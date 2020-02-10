import falcon
import subprocess
from marshmallow import fields, Schema

class CodeSchema(Schema):
    cmds = fields.List(Fields.String())

class CodeResource(object):
    schema = CodeSchema()

    def __init__(self, status):
        self.status = status


    def on_post(self, req, resp):
        for cmd in req.context['json']:
            process = subprocess.run(cmd.exe, cmd.args, check=True, stdout=subprocess.PIPE, universal_newlines=True)
        req.context['result'] =
