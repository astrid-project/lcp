class Negotiation_Middleware(object):
    def process_request(self, req, resp):
        resp.content_type = req.content_type
