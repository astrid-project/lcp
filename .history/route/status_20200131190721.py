import falcon
import uuid
import requests

class Status(object):
    def __init__(self, cb_host, cb_port):
        self.data = {
            'id': str(uuid.uuid1()),
            'registered': False,
            'agents': []
        }
        reg_data = {
            'hostname': 'x', # TODO
            'id': self.data['id'],
            'type_id': 'x' # TODO
        }
        reg_resp = requests.post(f'http://{cb_host}:{cb_port}/config/exec-env', json=reg_data)
        if reg_resp.status_code == 200 or reg_resp.status_code == 201:
            resp_data = response.json()
            self.data['alive'] = resp_data['when']
            self.data['registered'] = True
        print(f'Execute Environment ID: {self.data["id"]} registered at {self.data["alive"]}')

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.media = self.data
