import falcon
import uuid
import requests

class Status(object):
    def __init__(self, cb_host, cb_port):
        self.id = uuid.uuid1()
        data = {
            'hostname': 'x', # TODO
            'id': str(self.id),
            'type_id': 'x' # TODO
        }
        response = requests.post(f'http://{cb_host}:{cb_port}/config/exec-env', json=data)
        if response.status_code == falcon.HTTP_200:
            resp_data = response.json()
            self.alive = resp_data['when']
        print(response.json())
        self.connected_to_cb = False
        self.agents = []
        print(f'Execute Environment ID: {self.id}')

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.media = {
            'id': str(self.id),
            'connected-to-cb': self.connected_to_cb,
            'agents': self.agents
        }
