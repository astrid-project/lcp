from app import api
from flask_restplus import fields, reqparse, Resource
from request import Request

filter_model = api.model('query-filter', {
    'property': fields.String(description='All the conditions must be satisfied', required=False),
    'expr': fields.Integer(description='At least on condition must be satisfied', required=False),
}, description='Conditions to TODO')

api.model('query-clause', {})
query_clause_model = api.model('query-clause', {
    #    'and': fields.List(fields.Nested(api.models.get('query-clause')), description='All the conditions must be satisfied', required=False),
    #    'or': fields.List(fields.Nested(api.models.get('query-clause')), description='At least on condition must be satisfied', required=False),
    #    'not': fields.Nested(api.models.get('query-clause'), description='The condition must be not satisfied', required=False),
    'lte': fields.Nested(filter_model, description='', required=False),
    'gte': fields.Nested(filter_model, description='', required=False),
    'lt': fields.Nested(filter_model, description='', required=False),
    'gt': fields.Nested(filter_model, description='', required=False),
    'equal': fields.Nested(filter_model, description='', required=False),
    'reg-exp': fields.Nested(filter_model, description='', required=False),
}, description='Conditions to filter data to return')

query_order_model = api.model('query-order', {
    'property': fields.String(description='Name of the property to use for the sort', required=False, example='name'),
    'mode': fields.String(description='In asc(ending) or desc(ening) mode', required=False, enum=['asc', 'desc']),
}, description='Sort the results')

query_limit_model = api.model('query-limit', {
    'from': fields.Integer(description='Start 0-based index of the results to filter', required=False, example=1),
    'to': fields.Integer(description='End 0-based index (included) of the results to filter', required=False, example=2),
}, description='Limit the number of results')

query_model = api.model('query', {
    'select': fields.List(fields.String(), description='Select the properties to return', required=False, example=['id', 'name']),
    'where': fields.Nested(query_clause_model, required=False),
    'order': fields.List(fields.Nested(query_order_model), required=False),
    'limit': fields.Nested(query_limit_model, required=False),
}, description='Represent the query request', additional_properties=False)


class Query:
    def __init__(self, target):
        self.target = target
        self.s = Search(index=target.Index.name)

    @staticmethod
    def resolve_property(prop):
        return '_id' if prop == 'id' else prop

    def select(self, required=False, allowed=True):
        data = Request.json(
            error=self.target.error.not_acceptable).get('select')
        path = ['select']
        if self.__check(what='select', value=data, required=required, allowed=allowed):
            self.__not_acceptable_type(
                what='select', value=data, expected=list)
            for prop in data:
                self.__not_acceptable_type(
                    what='property', value=prop, expected=str, path=path)
            self.s = self.s.source(list(map(self.resolve_property, data)))

    def where(self, required=False, allowed=True):
        data = Request.json(
            error=self.target.error.not_acceptable).get('where')
        if self.__check(what='where', value=data, required=required, allowed=allowed):
            self.__not_acceptable_type(what='where', value=data, expected=dict)
            self.s.query = self._where(data, path=['where'])

    def _where(self, clause, path):
        q = Q()
        known_operators = ['and', 'or', 'not', 'equal', 'wildcard',
                           'reg-exp', 'lt', 'lte', 'gt', 'gte']
        for op, sub_clauses in clause.items():
            self.__not_acceptable_choice(
                what='operator', value=op, expected=known_operators, path=path)
            if op in ['and', 'or']:
                self.__not_acceptable_type(
                    what=op, value=sub_clauses, expected=list, path=path + [op])
            else:
                self.__not_acceptable_type(
                    what=op, value=sub_clauses, expected=dict, path=path + [op])
            if op == 'and':
                for sub_cls in sub_clauses:
                    q = q & self._where(sub_cls, path=path + [op])
            elif op == 'or':
                for sub_cls in sub_clauses:
                    q = q | self._where(sub_cls, path=path + [op])
            elif op == 'not':
                q = ~self._where(sub_clauses, path=path + [op])
            else:
                prop = self.resolve_property(sub_clauses.pop('property', None))
                expr = sub_clauses.pop('expr', None)
                self.__not_found(what='property', value=prop, path=path)
                self.__not_acceptable_type(
                    what='property', value=prop, expected=str, path=path)
                self.__not_found(what='expr', value=expr, path=path)
                self.__unknown(fields=sub_clauses, path=path)
                if op == 'equal':
                    q = Q('term', **{prop: expr})
                elif op == 'reg-exp':
                    q = Q('regexp', **{prop: dict(value=expr)})
                elif op == 'wildcard':
                    q = Q('wildcard', **{prop: dict(value=expr)})
                elif op in ['lt', 'lte', 'gt', 'gte']:
                    q = Q('range', **{prop: {op: expr}})
        return q

    def order(self, required=False, allowed=True):
        data = Request.json(
            error=self.target.error.not_acceptable).get('order')
        path = ['order']
        if self.__check(what='order', value=data, required=required, allowed=allowed):
            def make(item):
                prop = self.resolve_property(item.pop('property', None))
                mode = item.pop('mode', None)
                self.__not_found(what='property', value=prop, path=path)
                self.__not_acceptable_type(
                    what='property', value=prop, expected=str, path=path)
                self.__not_found(what='mode', value=mode, path=path)
                self.__not_acceptable_choice(what='mode', value=mode, expected=[
                    'asc', 'desc'], path=path)
                self.__unknown(fields=item, path=path)
                return {prop: {'order': mode}}
            self.s = self.s.sort(*list(map(make, data)))

    def limit(self, required=False, allowed=True):
        data = Request.json(
            error=self.target.error.not_acceptable).get('limit')
        path = ['order']
        if self.__check(what='limit', value=data, required=required, allowed=allowed):
            start = data.pop('from', None)
            end = data.pop('to', None)
            self.__not_found_all_of(
                what_value={'start': start, 'end': end}, path=path)
            if end is None:
                self.s = self.s[0:]
            else:
                start = 0
                self.s = self.s[start: (end + 1)]

    def get(self):
        return self.s

    def __check(self, what, value, path=None, required=True, allowed=True):
        if value is None:
            if required:
                self.target.error.not_found(
                    message=f'Not found', what=what, path=path)
            return False
        elif not allowed:
            self.target.error.not_acceptable(
                message=f'Not acceptable', what=what, value=value, path=path)
        return True

    def __not_found(self, what, value, path=None):
        if value is None:
            self.target.error.not_found(
                message=f'Not found', what=what, path=path)

    def __not_found_all_of(self, what_value, path=None):
        if all([value is None for value in what_value.values()]):
            self.target.error.not_found(
                message=f'At least one must be present', what=what_value.keys(), path=path)

    def __unknown(self, fields, path):
        for k, v in fields.items():
            self.target.error.not_acceptable(
                message='Unknown field', what=k, value=v, path=path)

    def __not_acceptable_type(self, what, value, expected, path=None,):
        if not isinstance(value, expected):
            self.target.error.not_acceptable(
                message='Not acceptable type', what=what, value=value, type=type(value).__name__, expected=expected.__name__, path=path)

    def __not_acceptable_choice(self, what, value, expected, path=None):
        if not value in expected:
            self.target.error.not_acceptable(
                message='Not acceptable value', what=what, value=value, expected=expected, path=path)
