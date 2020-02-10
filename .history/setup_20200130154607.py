# cspell:ignore unauth

from document import Document
from error import Error
from flask_api import status
from flask_restplus import fields
from query import query_model


class Setup:
    def __init__(self, target, namespace, model):
        self.target = target
        self.namespace = namespace
        self.model = model

    def route(self, func):
        return self.namespace.route(f'/{self.target.get_url()}')(func)

    def route_root(self, func):
        return self.namespace.route('/')(func)

    def route_selected(self, func):
        return self.namespace.route(f'/{self.target.get_url()}/{self.target.get_id_url()}')(func)

    def accepted(self, func):
        return {
            'delete': self.namespace.response(status.HTTP_202_ACCEPTED, f'{self.target.LABEL}s correctly deleted', Document.response_model),
            'put': self.namespace.response(status.HTTP_202_ACCEPTED, f'{self.target.LABEL} with the given ID correctly updated', Document.response_model)
        }.get(func.__name__)(func)

    def doc(self, func):
        return {
            'delete': self.namespace.doc(description=f'Delete the {self.target.LABEL}s based on the query'),
            'get': self.namespace.doc(description=f'Get the list of all {self.target.LABEL}s'),
            'post': self.namespace.doc(description=f'Add a new {self.target.LABEL}'),
            'put': self.namespace.doc(description=f'Update the {self.target.LABEL} with the given ID')
        }.get(func.__name__)(func)

    def created(self, func):
        return self.namespace.response(status.HTTP_201_CREATED, f'{self.target.LABEL} correctly added', Document.response_model)(func)

    def conflict(self, func):
        return self.namespace.response(status.HTTP_409_CONFLICT, f'{self.target.LABEL} with the same ID already found', Error.found_model)(func)

    def headers(self, func):
        out = func
        for k, v in Document.HEADERS.items():
            out = self.namespace.header(k, v)(out)
        return out

    def input(self, func):
        return {
            'delete': self.namespace.expect(query_model, description=f'Filter the {self.target.LABEL}s to delete', required=True),
            'get': self.namespace.expect(query_model, description=f'Filter the {self.target.LABEL}s to return', required=False),
            'post': self.namespace.expect(self.model, description=f'{self.target.LABEL} to add', required=True),
            'put': self.namespace.expect(self.model, description=f'Data to update the {self.target.LABEL} with the given ID', required=True)
        }.get(func.__name__)(func)

    def not_acceptable(self, func):
        return self.namespace.response(status.HTTP_406_NOT_ACCEPTABLE, 'Request not acceptable', Error.not_acceptable_model)(func)

    def not_found(self, func):
        return {
            'get': self.namespace.response(status.HTTP_404_NOT_FOUND, f'{self.target.LABEL}s not found', Error.found_model),
            'delete': self.namespace.response(status.HTTP_404_NOT_FOUND, f'{self.target.LABEL}s not found', Error.found_model),
            'put': self.namespace.response(status.HTTP_404_NOT_FOUND, f'{self.target.LABEL} with the given ID not found', Error.found_model)
        }.get(func.__name__)(func)

    def ok(self, func):
        return {
            'get': self.namespace.response(status.HTTP_200_OK, f'List of {self.target.LABEL}s', fields.List(fields.Nested(self.model)))
        }.get(func.__name__)(func)

    def unauth(self, func):
        return self.namespace.response(status.HTTP_401_UNAUTHORIZED, 'Unauthorized operation', Error.unauth_op_model)(func)

    def forbidden(self, func):
        return self.namespace.response(status.HTTP_403_FORBIDDEN, 'Authentication required', Error.auth_model)(func)
