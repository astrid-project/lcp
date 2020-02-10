import falcon
import uuid

class Status(object):
    def __init__(self):
        self.id = uuid.uuid1()

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.media = {
            'id': str(self.id)
        }
