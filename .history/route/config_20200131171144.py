import falcon

class Config(object):
    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = self.__class__
