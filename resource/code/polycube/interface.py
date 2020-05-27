from json import dump
from reader.arg import ArgReader
from requests import post
from resource.code.polycube.base import Base


class Interface(Base):
    def detach(self, cube, interface):
        def proc():
            resp = post(f'{self.endpoint}/detach', dumps({'cube': cube, 'port': interface}),
                        timeout=ArgReader.db.polycube_timeout)
            resp.raise_for_status()
        self.error_(proc)

    def attach(self, cube, interface):
        def proc():
            resp = post(f'{self.endpoint}/attach', dumps({'cube': cube, 'port': interface}),
                        timeout=ArgReader.db.polycube_timeout)
            resp.raise_for_status()
        self.error_manager(proc)
