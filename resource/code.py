from docstring import docstring
from lib.http import HTTP_Method
from lib.polycube import Polycube
from lib.response import *
from operator import itemgetter as item_getter
from resource.base import Base_Resource
from schema.code import *
from schema.response import *
from utils.sequence import is_list, wrap
from utils.datetime import datetime_to_str


__all__ = [
    'Code_Resource'
]


class Code_Resource(Base_Resource):
    tag = {'name': 'code', 'description': 'Code injection at run-time.'}
    routes = '/code/{id}',
    cubes = []

    def __init__(self):
        self.polycube = Polycube()

    @docstring(source='code/post.yaml')
    def on_post(self, req, resp, id=None):
        req_data = req.media or {}
        resp_data, valid = Code_Request_Schema(many=is_list(req_data),
                                               method=HTTP_Method.POST).validate(data=req.media, id=id)
        if valid:
            req_data_wrap = wrap(req_data)
            if len(req_data_wrap) > 0:
                for data in req_data_wrap:
                    id, code, interface, metrics = item_getter('id', 'code',
                                                               'interface', 'metrics')(data)
                    if all([id, code, interface]):
                        pc = self.polycube.create(cube=id, code=code,
                                                  interface=interface, metrics=metrics)
                        if not pc.get('error', False):
                            self.cubes.append(id)
                            msg = f'Code with the id={id} correctly injected'
                            resp_data = Created_Response(msg)
                        else:
                            msg = f'Not possible to inject code with the id={id}'
                            resp_data = Unprocessable_Entity_Response(msg)
                        resp_data.update(pc)
                    else:
                        msg = f'Not possible to inject code with the id={id}'
                        resp_data = Unprocessable_Entity_Response(msg)
                    resp_data.add(resp)
            else:
                msg = f'No content to create code with the {{request}}'
                No_Content_Response(msg, request=req_data).apply(resp)
        else:
            resp_data.apply(resp)

    @docstring(source='code/put.yaml')
    def on_put(self, req, resp, id=None):
        req_data = req.media or {}
        resp_data, valid = Code_Request_Schema(many=is_list(req_data),
                                               partial=True, method=HTTP_Method.PUT).validate(data=req.media, id=id)
        if valid:
            req_data_wrap = wrap(req_data)
            if len(req_data_wrap) > 0:
                for data in req_data_wrap:
                    id, code, interface, metrics = item_getter('id', 'code',
                                                               'interface', 'metrics')(data)
                    if all([id, code, interface]):
                        pc = self.polycube.update(cube=id, code=code,
                                                  interface=interface, metrics=metrics)
                        if not pc.get('error', False):
                            msg = f'Code with the id={id} correctly updated'
                            resp_data = Ok_Response(msg)
                        else:
                            msg = f'Not possible to update code with the id={id}'
                            resp_data = Unprocessable_Entity_Response(msg)
                        resp_data.update(pc)
                    else:
                        msg = f'Not possible to update code with the id={id}'
                        resp_data = Unprocessable_Entity_Response(msg)
                    resp_data.add(resp)
            else:
                msg = f'No content to update code with the {{request}}'
                No_Content_Response(msg, request=req_data).apply(resp)
        else:
            resp_data.apply(resp)

    @ docstring(source='code/post.yaml')
    def on_delete(self, req, resp, id=None):
        req_data = req.media or {}
        resp_data, valid = Code_Request_Schema(many=is_list(req_data),
                                               partial=True, method=HTTP_Method.DELETE).validate(data=req.media, id=id)
        if valid:
            req_data_wrap = wrap(req_data)
            if len(req_data_wrap) > 0:
                for data in req_data_wrap:
                    id = data.get('id', None)
                    if id is not None:
                        pc = self.polycube.delete(cube=id)
                        if not pc.get('error', False):
                            self.cubes.remove(id)
                            msg = f'Code with the id={id} correctly deleted'
                            resp_data = Reset_Content_Response(msg)
                        else:
                            msg = f'Not possible to delete code with the id={id}'
                            resp_data = Unprocessable_Entity_Response(msg)
                        resp_data.append(pc)
                    else:
                        msg = f'Not possible to update code with the id={id}'
                        resp_data = Unprocessable_Entity_Response(msg)
                    resp_data.add(resp)
            else:
                msg = f'No content to delete code with the {{request}}'
                No_Content_Response(msg, request=req_data).apply(resp)
        else:
            resp_data.apply(resp)
