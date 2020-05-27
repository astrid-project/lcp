from log import Log
from resource.code.polycube.check import Check
from resource.code.polycube.cube import Cube
from resource.code.polycube.interface import Interface
from reader.arg import ArgReader


def injection(cube, code, interface):
    host = ArgReader.db.polycube_host
    port = ArgReader.db.polycube_post
    endpoint = f'http://{host}:{port}/polycube/v1'

    log = Log.get('polycube')

    check = Check(endpoint)
    check.connection(endpoint)
    service = check.service_exists(endpoint, cube)

    cube_obj = Cube(endpoint)
    iface = Interface(endpoint)
    if service is None:
        log.info('Create new cube {cube}.')
        cube_obj.create(endpoint, cube, code)
        iface.attach(endpoint, cube, interface)
    else:
        log.info('Cube {cube} found.')
        attached_iface = service.get('parent', None)
        if attached_iface is None:
            iface.attach(cube, cube)
            if attached_iface != interface:
                iface.detach(cube, attached_iface)
                iface.attach(cube, interface)
        else:
            cube_obj.inject(cube, code)
