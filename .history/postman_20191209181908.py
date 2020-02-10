# cspell:ignore unauth

from app import api, ns_export as ns
from setup import Setup
from document import BaseObject
from flask_api import status
from resource import Resource


class Postman(BaseObject):
    LABEL = 'Postman'


setup = Setup(target=Postman, namespace=ns, model=None)


@setup.route
@setup.unauth
@setup.forbidden
@setup.headers
class PostmanResource(Resource):
    def get(self):
        return api.as_postman(urlvars=False, swagger=True), status.HTTP_200_OK
