from falcon.errors import HTTPGatewayTimeout as HTTP_Gateway_Timeout, HTTPServiceUnavailable as HTTP_Service_Unavailable
from json import loads
from reader.arg import Arg_Reader
from requests import get as get_req, post as post_req, put as put_req, delete as delete_req, HTTPError as HTTP_Error
from requests.exceptions import ConnectionError as Connection_Error, Timeout as Timeout_Error
from utils.log import Log

__all__ = [
    'Polycube'
]


class Polycube:
    def __init__(self):
        self.host = Arg_Reader.db.polycube_host
        self.port = Arg_Reader.db.polycube_port
        self.timeout = Arg_Reader.db.polycube_timeout
        self.endpoint = f'http://{self.host}:{self.port}/polycube/v1'
        self.log = Log.get('polycube')

        self.log.info(f'Check connection to {self.endpoint}')
        try:
            resp_req = get_req(self.endpoint,
                               timeout=Arg_Reader.db.polycube_timeout)
            self.__manager(resp_req)
        except (Connection_Error, HTTP_Error) as e:
            self.log.exception(f'Connection with polycube at {self.host}:{self.port} not possible', e)

    def get(self, cube):
        self.log.info(f'Get info of cube {cube}')
        try:
            resp_req = get_req(f'{self.endpoint}/dynmon/{cube}',
                               timeout=self.timeout)
            self.__manager(resp_req)
            return loads(resp_req.content)
        except HTTP_Error:
            return None

    def create(self, cube, code, interface, metrics):
        data = dict(name=cube, code=code, interface=interface, metrics=metrics)
        if self.get(cube) is None:
            self.log.info(f'Create cube {cube}.')
            attached_info = {}
            try:
                resp_req = put_req(f'{self.endpoint}/dynmon/{cube}',
                                   json={ 'dataplane-config': self.__dataplane_config(cube, code, metrics) },
                                   timeout=self.timeout)
                attached_info = self.__attach(cube, interface)
                return dict(status='created',
                            attached_info=attached_info, detached_info={},
                            data=data, **self.__from_resp(resp_req))
            except Exception as e:
                self.log.exception(f'Cube {cube} not created', e)
                return dict(status='error',
                            interface=attached_info, detached_info={},
                            data=data, **self.__from_resp(resp_req))
        else:
            return dict(error=True, description=f'Cube {cube} found.', data=data)

    def delete(self, cube):
        data = dict(cube=cube)
        if self.get(cube) is not None:
            self.log.info(f'Delete cube {cube}.')
            try:
                resp_req = delete_req(f'{self.endpoint}/dynmon/{cube}',
                                      timeout=self.timeout)
                self.__manager(resp_req)

                return dict(status='deleted',
                            data=data, **self.__from_resp(resp_req))
            except Exception as e:
                self.log.exception(f'Cube {cube} not deleted', e)
                return dict(error=True,
                            data=data, **self.__from_resp(resp_req))
        else:
            return dict(error=True, description=f'Cube {cube} not found.', data=data)

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
                resp_req = put_req(f'{self.endpoint}/dynmon/{cube}/dataplane-config',
                                   json=self.__dataplane_config(cube, code, metrics),
                                   timeout=self.timeout)
                self.__manager(resp_req)
                return dict(status='updated', attached_info=attached_info, detached_info=detached_info,
                            data=data, **self.__from_resp(resp_req))
            except Exception as e:
                self.log.exception(f'Cube {cube} not updated', e)
                return dict(status='error', attached_info=attached_info, detached_info=detached_info,
                            data=data, **self.__from_resp(resp_req))
        else:
            return dict(error=True, description=f'Cube {cube} not found.', data=data)

    @staticmethod
    def __dataplane_config(cube, code, metrics):
        return {
            'ingress-path': {
                'name': cube,
                'code': code,
                'metric-configs': metrics
            },
            'egress-path': {}
        }

    def __from_resp(self, resp):
        if resp.content:
            try:
                return loads(resp.content)
            except Exception:
                return dict(error=resp.status_code >= 400, message=resp.content.decode("utf-8"))
        else:
            return dict(error=resp.status_code >= 400)

    def __detach(self, cube, interface):
        resp_req = post_req(f'{self.endpoint}/detach',
                            json=dict(cube=cube, port=interface), timeout=self.timeout)
        self.__manager(resp_req)
        return dict(status='detached', data=dict(cube=cube, interface=interface),
                    **self.resp_from_resp(resp_req))

    def __attach(self, cube, interface):
        resp_req = post_req(f'{self.endpoint}/attach',
                            json=dict(cube=cube, port=interface), timeout=self.timeout)
        self.__manager(resp_req)
        return dict(status='attached', data=dict(cube=cube, interface=interface),
                    **self.resp_from_resp(resp_req))

    def __manager(self, resp_req):
        try:
            resp_req.raise_for_status()
        except Connection_Error as e:
            msg = f'Connection to Polycube at {self.endpoint} not possible'
            self.log.exception(msg, e)
            if resp_req.content:
                self.log.error(f'Response: {resp_req.content}')
            raise HTTP_Service_Unavailable(title='Connection error', description=msg)
        except Timeout_Error as e:
            to = Arg_Reader.db.polycube_timeout
            msg = f'Timely response not received from polycube at {self.endpoint} in {to} seconds.'
            self.log.exception(msg, e)
            if resp_req.content:
                self.log.error(f'Response: {resp_req.content}')
            raise HTTP_Gateway_Timeout(
                title='Polycube Unavailable', description=msg)
