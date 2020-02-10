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
        res = []
        for code in req.context['json']:
            process = subprocess.run(cmd.cmds, check=True, stdout=subprocess.PIPE, universal_newlines=True)
            res.append({
                'when': 'TODO',
                'out': process.stdout,
                'err': process.stderr,
                'status': 'TODO',
            })
        req.context['result'] =
