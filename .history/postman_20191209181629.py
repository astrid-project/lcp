from app import api, ns_export as ns
from config import Config
from document import BaseObject
from flask_api import status
from resource import Resource


class Postman(BaseObject):
    LABEL = 'Postman'


cnf = Config(target=Postman, namespace=ns, model=None)


@cnf.route
@cnf.unauth
@cnf.forbidden
@cnf.headers
class PostmanResource(Resource):
    def get(self):
        return api.as_postman(urlvars=False, swagger=True), status.HTTP_200_OK
