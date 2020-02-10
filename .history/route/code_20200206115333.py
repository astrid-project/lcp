from .base import Baseesource
from datetime import datetime
from schema import CodeRequest, CodeResponse
import falcon
import subprocess


class CodeResource(BaseResource):
    request_schema = CodeRequest()
    response_schema = CodeResponse()

    route = ['/code']

    def on_post(self, req, resp):
        res = {
            'when': datetime.now().strftime("%Y/%m/%d-%H:%M:%S"),
            'cmds': [],
            'return-code': 0
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
            res['return-code'] = res['return-code'] | process.returncode
        req.context['result'] = res
