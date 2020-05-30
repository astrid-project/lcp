from json import loads
from reader.arg import ArgReader
from requests import get as get_req, HTTPError
from utils.log import Log


class Polycube:
    from resource.code.polycube.error import request_manager
    from resource.code.polycube.interface import attach, detach

    from resource.code.polycube.create import create
    from resource.code.polycube.update import update
    from resource.code.polycube.delete import delete

    def __init__(self):
        self.host = ArgReader.db.polycube_host
        self.port = ArgReader.db.polycube_port
        self.timeout = ArgReader.db.polycube_timeout
        self.endpoint = f'http://{self.host}:{self.port}/polycube/v1'
        self.log = Log.get('polycube')

        self.log.info(f'Check connection to {self.endpoint}')
        resp_req = get_req(self.endpoint, timeout=ArgReader.db.polycube_timeout)
        self.request_manager(resp_req)

    def get(self, cube):
        self.log.info(f'Get info of cube {cube}')
        try:
            resp_req = get_req(f'{self.endpoint}/dynmon/{cube}',
                               timeout=self.timeout)
            self.request_manager(resp_req)
            return loads(resp_req.content)
        except HTTPError:
            return None

    def resp_from_resp(self, resp):
        return loads(resp.content) if resp.content else {}
