from docstring import docstring
from falcon.errors import HTTPBadRequest
from resource.code.polycube import Polycube
from utils.data import get_data
from utils.datetime import datetime_to_str
from utils.sequence import wrap


#@docstring(source='code/post.yaml') #FIXME
def on_delete(self, req, resp):
    json = req.context.get('json', None)
    if json is not None:
        polycube = Polycube()
        req_ctx_res = dict(when=datetime_to_str(), results=[])

        for data in wrap(json):
            id, output = get_data(data, 'id')
            if id is not None:
                output.update(polycube.delete(cube=id))
            req_ctx_res['results'].append(output)

        req.context['result'] = req_ctx_res
    else:
        raise HTTPBadRequest(title='Not valid JSON',
                             description='The request body is not a valid JSON or it is not encoded as UTF-8.')
