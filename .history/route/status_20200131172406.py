import falcon
import uuid

class Status(object):
    def __init__(self):
        self.id = uuid.uuid1()
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
