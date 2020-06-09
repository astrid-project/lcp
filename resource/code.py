from resource.base import BaseResource
from lib.polycube import Polycube
from schema.code import CodeRequestSchema, CodeResponseSchema
from schema.http_error import HTTPErrorSchema
from schema.validate import validate
from docstring import docstring


class CodeResource(BaseResource):
    tag = {'name': 'code', 'description': 'Code injection at run-time.'}
    routes = '/code/{id}',
    cubes = []

    def __init__(self):
        self.polycube = Polycube()

    @docstring(source='code/post.yaml')
    def on_post(self, req, resp, id=None):
        req_data = validate(schema=CodeRequestSchema(), method='POST', check_unique_id=True, data=req.media, id=id)
        resp_data = dict(when=datetime_to_str(), results=[])
        for data in wrap(req_data):
            id, code, interface, metrics, output = get_data(
                data, 'id', 'code', 'interface', 'metrics')
            if all([id, code, interface]):
                output.update(self.polycube.create(cube=id, code=code,
                                                   interface=interface, metrics=metrics))
            resp_data['results'].append(output)
            if not output.get('error', False):
                self.cubes.append(id)
        resp.media = validate(schema=CodeResponseSchema(), data=resp_data)

    @docstring(source='code/put.yaml')
    def on_put(self, req, resp, id=None):
        req_data = validate(schema=CodeRequestSchema(), method='PUT', check_unique_id=True, data=req.media, id=id)
        resp_data = dict(when=datetime_to_str(), results=[])
        for data in wrap(req_data):
            id, code, interface, metrics, output = get_data(
                data, 'id', 'code', 'interface', 'metrics')
            if all([id, code, interface]):
                output.update(self.polycube.update(cube=id, code=code,
                                                   interface=interface, metrics=metrics))
            resp_data['results'].append(output)
        resp.media = validate(schema=CodeResponseSchema(), data=resp_data)

    @docstring(source='code/post.yaml')
    def on_delete(self, req, resp, id=None):
        req_data = validate(schema=CodeRequestSchema(), method='DELETE', check_unique_id=True, data=req.media, id=id)
        resp_data = dict(when=datetime_to_str(), results=[])
        for data in wrap(req_data):
            id, output = get_data(data, 'id')
            if id is not None:
                output.update(self.polycube.delete(cube=id))
            resp_data['results'].append(output)
            if not output.get('error', False):
                self.cubes.remove(id)
        resp.media = validate(schema=CodeResponseSchema(), data=resp_data)
