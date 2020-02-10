import falcon

class Status(object):
    def __init__()

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = 'Ciao'
