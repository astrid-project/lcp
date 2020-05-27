from reader.arg import ArgReader
from requests import get
from requests.exceptions import ConnectionError, HTTPError as HTTPErrorReq, RequestException, Timeout
from resource.code.polycube.base import Base


class Check(Base):
    def connection(self):
        def proc():
            get(self.endpoint, timeout=ArgReader.db.polycube_timeout)
        self.error_manager(proc)

    def service_exists(cube):
        def proc():
            try:
                resp = get(f'{self.endpoint}/dynmon/{cube}',
                           timeout=ArgReader.db.polycube_timeout)
                resp.raise_for_status()
                return loads(resp.content)
            except HTTPErrorReq:
                return None
        return self.error_manager(proc)
