from requests import put as put_req


def create(self, cube, code, interface, metrics):
    data = dict(name=cube, code=code, interface=interface, metrics=metrics)
    if self.get(cube) is None:
        self.log.info(f'Create cube {cube}.')
        attached_info = {}
        try:
            body_req = dict(dataplane=dict(name=cube, code=code, metrics=metrics))
            resp_req = put_req(f'{self.endpoint}/dynmon/{cube}', json=body_req, timeout=self.timeout)

            attached_info = self.attach(cube, interface)

            return dict(status='created',
                        description='Cube [cube] created',
                        attached_info=attached_info, detached_info={},
                        data=data,
                        polycube_response=self.resp_from_resp(resp_req))

        except Exception as exception:
            self.log.error(f'Exception: {exception}')
            return dict(status='error',
                        description='Cube [cube] not created',
                        interface=attached_info, detached_info={},
                        data=data,
                        polycube_response=self.resp_from_resp(resp_req))
    else:
        return dict(error=True,
                    description='Cube [cube] found.',
                    data=data)
