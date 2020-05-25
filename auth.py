from resource.status import StatusResource
from utils import hash


def auth(dev_username, dev_password):
    def handler(username, password):
        auth_data = [(dev_username, dev_password)]
        auth_data.extend(zip(StatusResource.auth_db.keys(), StatusResource.auth_db.values()))
        if (username, hash(password)) in auth_data:
            return {'username': username}
        else:
            False
    return handler
