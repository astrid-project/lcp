from datetime import datetime
import falcon
import subprocess

class CodeSchema(Schema):
    cmds = fields.List(fields.Nested(CmdSchema()))

class CodeResource(object):

    def __init__(self, status):
        self.status = status

    def on_post(self, req, resp):
        res = {
            'when': datetime.now().strftime("%Y/%m/%d-%H:%M:%S"),
            'cmds': []
        }
        code = req.context['json']
        for cmd in code['cmds']:
            process = subprocess.run(cmd['prog'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            res['cmds'].append({
                'when': datetime.now().strftime("%Y/%m/%d-%H:%M:%S"),
                'cmd': cmd['prog'],
                'args': cmd['args'],
                'stdout': process.stdout,
                'stderr': process.stderr,
                'return-code': process.returncode
            })
        req.context['result'] = res
