from datetime import datetime
import falcon
from marshmallow import fields, Schema
import uuid


class StatusResponseSchema(Schema):
    when = fields.DateTime()
    cmds = fields.List(fields.Nested(CmdResponseScheme()))
    return_code = fields.Integer()


class Status(object):
    response_schema = StatusResponseSchema()

    def __init__(self, cb_host, cb_port):
        self.data = {
            'id': uuid.uuid1())
            'agents': [],
            ''
        }
        # reg_resp = requests.post(f'http://{cb_host}:{cb_port}/config/exec-env', json=reg_data)
        # print(reg_resp.status_code)
        # if reg_resp.status_code == 200 or reg_resp.status_code == 201:
        #     resp_data = reg_resp.json()
        #     self.data['alive'] = resp_data['when']
        #     self.data['registered'] = True
        # elif reg_resp.status_code == 409:
        #     reg_resp = requests.post(f'http://{cb_host}:{cb_port}/config/exec-env', json={"where"})
        # print(f'Execute Environment {self.data["id"]} registered at {self.data["alive"]}')

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.media = self.data
