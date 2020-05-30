from requests import delete as delete_req


def delete(self, cube):
    data = dict(cube=cube)
    if self.get(cube) is not None:
        self.log.info(f'Delete cube {cube}.')
        try:
            resp_req = delete_req(f'{self.endpoint}/dynmon/{cube}', timeout=self.timeout)
            self.request_manager(resp_req)

            return dict(status='deleted',
                        description=f'Cube {cube} deleted',
                        data=data,
                        polycube_response=self.resp_from_resp(resp_req))
        except Exception as exception:
            self.log.error(f'Exception: {exception}')
            return dict(error=True,
                        description=f'Cube [cube] not deleted.',
                        data=data,
                        polycube_response=self.resp_from_resp(resp_req))
    else:
        return dict(error=True,
                    description=f'Cube [cube] not found.',
                    data=data)
