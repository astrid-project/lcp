from json import dumps, loads
from reader.arg import ArgReader
from requests import post as post_req


def detach(self, cube, interface):
    data = dict(cube=cube, interface=interface)

    body_req = dict(cube=cube, port=interface)
    resp_req = post_req(f'{self.endpoint}/detach', json=body_req, timeout=self.timeout)
    self.request_manager(resp_req)

    return dict(status='detached',
                description='Cube [cube] detached from interface [interface]',
                data=data,
                polycube_response=self.resp_from_resp(resp_req))


def attach(self, cube, interface):
    data = dict(cube=cube, interface=interface)

    body_req = dict(cube=cube, port=interface)
    resp_req = post_req(f'{self.endpoint}/attach', json=body_req, timeout=self.timeout)
    self.request_manager(resp_req)

    return dict(status='attached',
                description='Cube [cube] attached to interface [interface]',
                data=data,
                polycube_response=self.resp_from_resp(resp_req))
