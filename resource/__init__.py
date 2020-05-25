from resource.code import CodeResource
from resource.config import ConfigResource
from resource.status import StatusResource

from log import Log
from utils import wrap


db = (
    CodeResource,
    ConfigResource,
    StatusResource
)

tags = []
for Resource in db:
    tags.append(Resource.tag)


def routes(api, spec):
    log = Log.get('resource')
    for Resource in db:
        resource = Resource()
        for route in wrap(Resource.routes):
            api.add_route(route, resource)
            spec.path(resource=resource)
            log.success(f'{route} endpoint configured')
