# cspell:ignore dasherize strftime

from app import api, log
from datetime import datetime
from error import Error
from flask_restplus import fields
from flask_api import status
import inflection
from query import Query
from request import Request


class BaseObject:
    ALL = '__ALL__'

    @staticmethod
    def get_id_url():
        return '<string:id>'

    @classmethod
    def get_url(cls):
        return inflection.dasherize(fields.camel_to_dash(cls.__name__))


class BaseDocument(BaseObject):
    HEADERS = {'Powered-by': 'ASTRID'}

    @classmethod
    def setup(cls):
        cls.error = Error(cls)
        return cls


class Document(BaseDocument):
    DESC = {
        status.HTTP_201_CREATED: 'created',
        status.HTTP_202_ACCEPTED: 'accepted',
        status.HTTP_404_NOT_FOUND: 'not-found'
    }

    response_model = api.model('response-data', {
        'when': fields.DateTime(description='Execution datetime', required=True),
        'target': fields.String(description='Target object', required=True),
        'action': fields.String(description='Execution action', required=True),
        'success': fields.Boolean(description='Execution performed with success or not', required=True)
    }, description='Response Data object')

    @staticmethod
    def get_data(obj):
        return dict(obj.to_dict(), id=obj.meta.id)

    @classmethod
    def setup(cls):
        super().setup()
        cls.init()
        return cls

    @classmethod
    def __response(cls, http_status_code, action, **kwargs):
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        if status.is_client_error(http_status_code):
            type = 'client-error'
        elif status.is_informational(http_status_code):
            type = 'informational'
        elif status.is_redirect(http_status_code):
            type = 'redirect'
        elif status.is_server_error(http_status_code):
            type = 'server-error'
        elif status.is_success(http_status_code):
            type = 'success'
        out = {
            'when': datetime.now().strftime('%Y/%m/%d-%H:%M:%S'),
            'target': cls.get_url(),
            'type': type,
            'status': cls.DESC.get(http_status_code, 'unknown'),
            'action': action,
            'success': True
        }
        out.update(kwargs)
        return out, http_status_code, cls.HEADERS

    @classmethod
    def read(cls):
        q = Query(cls)
        q.select()
        q.where()
        q.order()
        q.limit()
        s = q.get()
        res = s.execute()
        return [cls.get_data(item) for item in res], status.HTTP_200_OK, cls.HEADERS

    @classmethod
    def created(cls):
        data = Request.json(error=cls.error.not_acceptable)
        if hasattr(cls, 'apply'):
            cls.apply(data)
        id = data.pop('id', None)
        if id is None:
            cls.error.not_found(message='Missing ID', what='id')
        try:
            cls.get(id=id)
        except elasticsearch.NotFoundError:
            res = cls(meta={'id': id}, **data).save()
            return cls.__response(status.HTTP_201_CREATED if res else status.HTTP_304_NOT_MODIFIED, action='create', success=res)
        else:
            cls.error.conflict(message='ID already found', what='id', value=id)

    @classmethod
    def updated(cls, id):
        data = Request.json(error=cls.error.not_acceptable)
        try:
            cls.get(id=id).update(**data)
            return cls.__response(status.HTTP_202_ACCEPTED, action='update', success=True)
        except elasticsearch.NotFoundError:
            cls.error.not_found(message='ID not found', what='id', value=id)

    @classmethod
    def deleted(cls):
        try:
            q = Query(cls)
            q.select(allowed=False)
            q.where(required=True)
            q.order(allowed=False)
            q.select(allowed=False)
            res = q.get().delete()
            return cls.__response(status.HTTP_202_ACCEPTED if res.deleted > 0 else status.HTTP_404_NOT_FOUND, action='delete', success=res.deleted > 0, **res.to_dict())
        except elasticsearch.RequestError as e:
            cls.error.request(e)
