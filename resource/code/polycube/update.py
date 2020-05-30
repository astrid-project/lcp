from requests import put as put_req


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
                attached_info = self.attach(cube, cube)
            elif attached_iface != interface:
                attached_info = self.detach(cube, attached_iface)
                detached_info = self.attach(cube, interface)

            body_req = dict(name=cube, code=code, metrics=metrics)
            resp_req = put_req(f'{self.endpoint}/dynmon/{cube}/dataplane', json=body_req, timeout=self.timeout)
            self.request_manager(resp_req)

            return dict(status='updated',
                        description='Cube [cube] updated',
                        attached_info=attached_info, detached_info=detached_info,
                        data=data,
                        polycube_response=self.resp_from_resp(resp_req))

        except Exception as exception:
            self.log.error(f'Exception: {exception}')
            return dict(status='error',
                        description='Cube [cube] not updated',
                        attached_info=attached_info, detached_info=detached_info,
                        data=data,
                        polycube_response=self.resp_from_resp(resp_req))
    else:
        return dict(error=True,
                    description=f'Cube [cube] not found.',
                    data=data)
