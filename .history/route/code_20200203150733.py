import falcon
import subprocess
from marshmallow import fields, Schema

class CodeSchema(Schema):
    cmds = fields.List(fields.List())

class CodeResource(object):
    schema = CodeSchema()

    def __init__(self, status):
        self.status = status


    def on_post(self, req, resp):
        res = []
        for code in req.context['json']:
            process = subprocess.run(code.cmds, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            res.append({
                'when': 'TODO',
                'out': process.stdout,
                'err': process.stderr,
                'status': 'TODO',
            })
        req.context['result'] = res
