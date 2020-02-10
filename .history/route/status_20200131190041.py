import falcon
import uuid
import requests

class Status(object):
    def __init__(self, cb_host, cb_port):
        self.data = {
            id: str(uuid.uuid1())
        }
        reg_data = {
            'hostname': 'x', # TODO
            'id': str(self.id),
            'type_id': 'x' # TODO
        }
        reg_resp = requests.post(f'http://{cb_host}:{cb_port}/config/exec-env', json=reg_data)
        if reg.status_code == falcon.HTTP_200:
            resp_data = response.json()
            self.data['alive'] = resp_data['when']
            self.registered = True
        self.agents = []
        print(f'Execute Environment ID: {self.id}')

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.media = self.data
