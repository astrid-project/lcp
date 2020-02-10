import falcon
import subprocess
from marshmallow import fields, Schema

class CmdSchema(Schema):
    prog = fields.String()
    args = fields.List(fields.String())

class CodeSchema(Schema):
    cmds = fields.List(fields.Nested(CmdSchema()))

class CodeResource(object):
    schema = CodeSchema()

    def __init__(self, status):
        self.status = status


    def on_post(self, req, resp):
        res = []
        for cmd in req.context['json']:
            print(cmd)
            process = subprocess.run(cmd.prog, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            res.append({
                'when': 'TODO',
                'out': process.stdout,
                'err': process.stderr,
                'status': 'TODO',
            })
        req.context['result'] = res
