from docstring import docstring
from falcon.errors import HTTPBadRequest
from resource.code.polycube import Polycube
from utils.data import get_data
from utils.datetime import datetime_to_str
from utils.sequence import wrap


#@docstring(source='code/post.yaml') #FIXME
def on_post(self, req, resp):
    json = req.context.get('json', None)
    if json is not None:
        polycube = Polycube()
        req_ctx_res = dict(when=datetime_to_str(), results=[])

        for data in wrap(json):
            id, code, interface, metrics, output = get_data(data, 'id', 'code', 'interface', 'metrics')
            if all([id, code, interface]):
                output.update(polycube.create(cube=id, code=code, interface=interface, metrics=metrics))
            req_ctx_res['results'].append(output)

        req.context['result'] = req_ctx_res
    else:
        raise HTTPBadRequest(title='Not valid JSON',
                             description='The request body is not a valid JSON or it is not encoded as UTF-8.')
