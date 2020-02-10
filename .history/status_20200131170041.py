import falcon
import uuid

class Status(object):
    def __init__(self):
        self.id =

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = 'Ciao'
