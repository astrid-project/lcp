from reader.arg import ArgReader
from requests import put
from resource.code.polycube.base import Base


class Cube(Base):
    def create(self, cube, code):
        def proc():
            resp = put(f'{self.endpoint}/dynmon/{cube}', dumps({'dataplane': code}),
                       timeout=ArgReader.db.polycube_timeout)
            resp.raise_for_status()
        self.error_manager(proc)

    def inject(cube, code):
        def proc():
            resp = put(f'{self.endpoint}/dynmon/{cube}/dataplane', dumps(code),
                       timeout=ArgReader.db.polycube_timeout)
            reps.raise_for_status()
        self.error_manager(proc)
