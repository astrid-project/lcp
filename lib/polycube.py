from falcon.errors import HTTPBadRequest, HTTPGatewayTimeout, HTTPServiceUnavailable
from json import loads
from reader.arg import ArgReader
from requests import get as get_req, post as post_req, put as put_req, delete as delete_req, HTTPError
from requests.exceptions import ConnectionError, Timeout
from utils.log import Log


class Polycube:
    def __init__(self):
        self.host = ArgReader.db.polycube_host
        self.port = ArgReader.db.polycube_port
        self.timeout = ArgReader.db.polycube_timeout
        self.endpoint = f'http://{self.host}:{self.port}/polycube/v1'
        self.log = Log.get('polycube')

        self.log.info(f'Check connection to {self.endpoint}')
        resp_req = get_req(self.endpoint,
                           timeout=ArgReader.db.polycube_timeout)
        self.__manager(resp_req)

    def get(self, cube):
        self.log.info(f'Get info of cube {cube}')
        try:
            resp_req = get_req(f'{self.endpoint}/dynmon/{cube}',
                               timeout=self.timeout)
            self.__manager(resp_req)
            return loads(resp_req.content)
        except HTTPError:
            return None

    def create(self, cube, code, interface, metrics):
        data = dict(name=cube, code=code, interface=interface, metrics=metrics)
        if self.get(cube) is None:
            self.log.info(f'Create cube {cube}.')
            attached_info = {}
            try:
                resp_req = put_req(f'{self.endpoint}/dynmon/{cube}',
                                   json=dict(dataplane=dict(name=cube,
                                                            code=code, metrics=metrics)),
                                   timeout=self.timeout)
                attached_info = self.__attach(cube, interface)
                return dict(status='created', description='Cube [cube] created',
                            attached_info=attached_info, detached_info={},
                            data=data, polycube_response=self.__from_resp(resp_req))
            except Exception as exception:
                self.log.error(f'Exception: {exception}')
                return dict(status='error', description='Cube [cube] not created',
                            interface=attached_info, detached_info={},
                            data=data, polycube_response=self.__from_resp(resp_req))
        else:
            return dict(error=True, description='Cube [cube] found.', data=data)

    def delete(self, cube):
        data = dict(cube=cube)
        if self.get(cube) is not None:
            self.log.info(f'Delete cube {cube}.')
            try:
                resp_req = delete_req(f'{self.endpoint}/dynmon/{cube}',
                                      timeout=self.timeout)
                self.__manager(resp_req)

                return dict(status='deleted', description=f'Cube {cube} deleted',
                            data=data, polycube_response=self.__from_resp(resp_req))
            except Exception as exception:
                self.log.error(f'Exception: {exception}')
                return dict(error=True, description=f'Cube [cube] not deleted.',
                            data=data, polycube_response=self.__from_resp(resp_req))
        else:
            return dict(error=True, description=f'Cube [cube] not found.', data=data)

    def update(self, cube, code, interface, metrics):
        data = dict(name=cube, code=code, interface=interface, metrics=metrics)
        service = self.get(cube)
        if service is not None:
            self.log.info(f'Update cube {cube}.')
            try:
                attached_iface = service.get('parent', None)
                attached_info = {}
                detached_info = {}
                if attached_iface is None:
                    attached_info = self.__attach(cube, cube)
                elif attached_iface != interface:
                    attached_info = self.__detach(cube, attached_iface)
                    detached_info = self.__attach(cube, interface)
                resp_req = put_req(f'{self.endpoint}/dynmon/{cube}/dataplane',
                                   json=dict(name=cube, code=code,
                                             metrics=metrics),
                                   timeout=self.timeout)
                self.__manager(resp_req)
                return dict(status='updated', description='Cube [cube] updated',
                            attached_info=attached_info, detached_info=detached_info,
                            data=data, polycube_response=self.__from_resp(resp_req))
            except Exception as exception:
                self.log.error(f'Exception: {exception}')
                return dict(status='error', description='Cube [cube] not updated',
                            attached_info=attached_info, detached_info=detached_info,
                            data=data, polycube_response=self.__from_resp(resp_req))
        else:
            return dict(error=True, description=f'Cube [cube] not found.', data=data)

    def __from_resp(self, resp):
        return loads(resp.content) if resp.content else {}

    def __detach(self, cube, interface):
        resp_req = post_req(f'{self.endpoint}/detach',
                            json=dict(cube=cube, port=interface), timeout=self.timeout)
        self.__manager(resp_req)
        return dict(status='detached', description='Cube [cube] detached from interface [interface]',
                    data=dict(cube=cube, interface=interface),
                    polycube_response=self.resp_from_resp(resp_req))

    def __attach(self, cube, interface):
        resp_req = post_req(f'{self.endpoint}/attach',
                            json=dict(cube=cube, port=interface), timeout=self.timeout)
        self.__manager(resp_req)
        return dict(status='attached', description='Cube [cube] attached to interface [interface]',
                    data=dict(cube=cube, interface=interface),
                    polycube_response=self.resp_from_resp(resp_req))

    def __manager(self, resp_req):
        try:
            resp_req.raise_for_status()
        except ConnectionError as conn_err:
            self.log.error(f'Exception: {conn_err}')
            if resp_req.content:
                self.log.error(f'response: {resp_req.content}')
            raise HTTPServiceUnavailable(title='Connection error',
                                         description=f'Connection to Polycube at {self.endpoint} not possible.')
        except Timeout as timeout:
            self.log.error(f'exception: {timeout}')
            if resp_req.content:
                self.log.error(f'response: {resp_req.content}')
            to = ArgReader.db.polycube_timeout
            raise HTTPGatewayTimeout(
                title='Polycube Unavailable',
                description=f'Timely response not received from polycube at {self.endpoint} in {to} seconds.')
