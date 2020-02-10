from datetime import datetime
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
        code = req.context['json']
        for cmd in code['cmds']:
            process = subprocess.run(cmd['prog'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            res.append({
                'when': datetime.now().strftime("%Y/%m/%d-%H:%M:%S"),
                'stdout': process.stdout,
                'stderr': process.stderr,
                'return-code': process.returncode,
            })
        print(res)
        req.context['result'
        req.context['result'] = res
