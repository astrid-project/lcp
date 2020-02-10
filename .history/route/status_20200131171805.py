import falcon
import uuid

class Status(object):
    def __init__(self):
        self.id = uuid.uuid1()
        print(f'Execute Environment start with ID: {self.id}')

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.media = {
            'id': str(self.id)
        }
