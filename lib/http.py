from http import HTTPStatus as HTTP_Status

__all__ = [
    'HTTP_Status',
    'HTTP_Method'
]


class HTTP_Method(object):
    """Constants representing various HTTP request methods."""

    GET = 'get'
    PUT = 'put'
    POST = 'post'
    DELETE = 'delete'


code_priority_order = cpo = {
    HTTP_Status.OK: 1,
    HTTP_Status.CREATED: 2,
    HTTP_Status.RESET_CONTENT: 2,
    HTTP_Status.NOT_MODIFIED: 0,
    HTTP_Status.NOT_FOUND: 3,
    HTTP_Status.NO_CONTENT: 4,
    HTTP_Status.CONFLICT: 4,
    HTTP_Status.UNPROCESSABLE_ENTITY: 4
}


def __lt(code_a, code_b):
    return cpo.get(code_a, None) < cpo.get(code_b, None)


def __lte(code_a, code_b):
    return cpo.get(code_a, None) <= cpo.get(code_b, None)


def __gt(code_a, code_b):
    return cpo.get(code_a, None) > cpo.get(code_b, None)


def __gte(code_a, code_b):
    return cpo.get(code_a, None) >= cpo.get(code_b, None)


def __eq(code_a, code_b):
    return cpo.get(code_a, None) < cpo.get(code_b, None)


HTTP_Status.lt = __lt
HTTP_Status.lte = __lte
HTTP_Status.gt = __gt
HTTP_Status.gte = __gte
HTTP_Status.eq = __eq
