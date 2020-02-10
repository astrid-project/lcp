# cspell:ignore unauth strftime jsonify

from app import api
from datetime import datetime
from flask import jsonify
from flask_api import status
from flask_restplus import abort, fields


class Error:
    DESC = {
        status.HTTP_400_BAD_REQUEST: 'bad-request',
        status.HTTP_404_NOT_FOUND: 'not-found',
        status.HTTP_406_NOT_ACCEPTABLE: 'not-acceptable',
        status.HTTP_409_CONFLICT: 'conflict',
    }

    unauth_op_model = api.model('unauthorized-operation-error-data', {
        'when': fields.DateTime(description='Response datetime', required=True),
        'message': fields.String(description='Human readable message that describes the error', required=True, example='Operation not allowed'),
    })

    auth_model = api.model('authentication-error-data', {
        'when': fields.DateTime(description='Response datetime', required=True),
        'message': fields.String(description='Human readeable message that describes the error', required=True, example='Authentication required'),
    })

    not_acceptable_property_model = api.model('not-acceptable-property-error-data', {
        'property': fields.String(description='Name of the property', required=True, example='hostname'),
        'reason': fields.String(description='Reason for what the value is not acceptable', required=True, example='missing'),
        'value': fields.String(description='Not acceptable value', required=False, example=3),
    })

    not_acceptable_model = api.model('not-acceptable-error-data', {
        'when': fields.DateTime(description='Response datetime', required=True),
        'message': fields.String(description='Human readeable message that describes the error', required=True, example='Request not acceptable'),
        'target': fields.String(description='Object target of the operation', required=True, example='ExecEnv'),
        'data': fields.List(fields.Nested(not_acceptable_property_model), description='List of not acceptable properties', required=True)
    })

    found_model = api.model('found-error-data', {
        'when': fields.DateTime(description='Response datetime', required=True),
        'message': fields.String(description='Human readeable message that describes the error', required=True, example='Network Link Type found'),
        'target': fields.String(description='Object name', required=True, example='NetworkLinkType'),
        'id': fields.String(description='ID of object instance', required=True, example='pnt-to-pnt')
    })

    exception_model = api.model('exception-error-data', {
        'when': fields.DateTime(description='Response datetime', required=True),
        'exception': fields.String(description='Exception message', required=True, example='Connection timeout')
    })

    def __init__(self, target):
        self.target = target

    def __abort(self, http_status_code, **kwargs):
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        when = kwargs.pop('when', datetime.now().strftime('%Y/%m/%d-%H:%M:%S'))
        target = kwargs.pop('target', self.target.get_url())
        if status.is_client_error(http_status_code):
            def_type = 'client-error'
        elif status.is_informational(http_status_code):
            def_type = 'informational'
        elif status.is_redirect(http_status_code):
            def_type = 'redirect'
        elif status.is_server_error(http_status_code):
            def_type = 'server-error'
        elif status.is_success(http_status_code):
            def_type = 'success'
        type = kwargs.pop('type', def_type)
        abort(http_status_code, when=when, target=target, type=type,
              status=self.DESC.get(http_status_code, 'unknown'), **kwargs)

    def not_found(self, **kwargs):
        self.__abort(status.HTTP_404_NOT_FOUND, **kwargs)

    def conflict(self, **kwargs):
        self.__abort(status.HTTP_409_CONFLICT, **kwargs)

    def not_acceptable(self, **kwargs):
        self.__abort(status.HTTP_406_NOT_ACCEPTABLE, **kwargs)

    def request(self, exception):
        self.__abort(exception.status_code,
                     message=exception.info['error']['reason'], error=exception.info['error']['type'])
