from lib.http import HTTP_Status
from utils.exception import extract_info
from utils.sequence import expand, is_list

import falcon

__all__ = [
    'Bad_Request_Response',
    'Conflict_Response',
    'Content_Response',
    'Created_Response',
    'Internal_Server_Error_Response',
    'No_Content_Response',
    'Not_Acceptable_Response',
    'Not_Found_Response',
    'Not_Modified_Response',
    'Ok_Response',
    'Reset_Content_Response',
    'Unauthorized_Response',
    'Unprocessable_Entity_Response',
    'Unsupported_Media_Type_Response'
]


class Base_Response(object):
    error = False

    def __init__(self, message, error=False, exception=None, **kwargs):
        self.data = dict(message=message)
        if exception is not None:
            self.data.update(exception=extract_info(exception))
        self.data.update(kwargs)

    def __data(self):
        return expand(self.data, status=self.status(), code=self.code, error=self.error)

    def __str__(self):
        return self.status()

    def __int__(self):
        return self.code

    def __dict__(self):
        return self.__data()

    @classmethod
    def status(cls):
        return cls.code.phrase

    def apply(self, resp):
        resp.media = self.__data()
        resp.status = f'{self.code} {self}'

    def add(self, resp):
        if is_list(resp):
            resp.append(self.__data())
        else:
            if not is_list(resp.media):
                resp.media = []
            resp.media.append(self.__data())
            resp_code = int(resp.status.split()[0])
            if self.code is not None and HTTP_Status.lt(resp_code, self.code):
                resp.status = f'{self.code} {self.status()}'

    def update(self, **kwargs):
        self.data.update(kwargs)


class Bad_Request_Response(Base_Response):
    code = HTTP_Status.BAD_REQUEST
    error = True

    def __init__(self, exception=None, **kwargs):
        super().__init__(exception.title if exception is not None else 'Request not valid',
                         exception=exception, **kwargs)


class Conflict_Response(Base_Response):
    code = HTTP_Status.CONFLICT
    error = True

    def __init__(self, message, exception=None, **kwargs):
        super().__init__(message, exception=exception, **kwargs)


class Created_Response(Base_Response):
    code = HTTP_Status.CREATED

    def __init__(self, message, **kwargs):
        super().__init__(message, **kwargs)


class Internal_Server_Error_Response(Base_Response):
    code = HTTP_Status.INTERNAL_SERVER_ERROR
    error = True

    def __init__(self, exception=None, **kwargs):
        super().__init__(exception.title if exception is not None else 'Server not available to satisfy the request',
                         exception=exception, **kwargs)


class Not_Acceptable_Response(Base_Response):
    code = HTTP_Status.NOT_ACCEPTABLE
    error = True

    def __init__(self, message, exception=None, **kwargs):
        super().__init__(message, exception=exception, **kwargs)


class No_Content_Response(Base_Response):
    code = HTTP_Status.NO_CONTENT

    def __init__(self, message, exception=None, **kwargs):
        super().__init__(message, exception=exception, **kwargs)


class Not_Found_Response(Base_Response):
    code = HTTP_Status.NOT_FOUND
    error = True

    def __init__(self, message, exception=None, **kwargs):
        super().__init__(message, exception=exception, **kwargs)


class Not_Modified_Response(Base_Response):
    code = HTTP_Status.NOT_MODIFIED

    def __init__(self, message, **kwargs):
        super().__init__(message, **kwargs)


class Ok_Response(Base_Response):
    code = HTTP_Status.OK

    def __init__(self, message, **kwargs):
        super().__init__(message, **kwargs)


class Content_Response(Ok_Response):
    def __init__(self, content):
        self.data = content


class Internal_Server_Error_Response(Base_Response):
    code = HTTP_Status.INTERNAL_SERVER_ERROR
    error = True

    def __init__(self, message, **kwargs):
        super().__init__(message, **kwargs)



class Reset_Content_Response(Base_Response):
    code = HTTP_Status.RESET_CONTENT

    def __init__(self, message, **kwargs):
        super().__init__(message, **kwargs)


class Unauthorized_Response(Base_Response):
    code = HTTP_Status.UNAUTHORIZED
    error = True

    def __init__(self):
        super().__init__(message='Authentication failed')

    def apply(self, resp):
        super().apply(resp)
        resp.complete = True


class Unprocessable_Entity_Response(Base_Response):
    code = HTTP_Status.UNPROCESSABLE_ENTITY
    error = True

    def __init__(self, message, exception=None, **kwargs):
        super().__init__(message, exception=exception, **kwargs)


class Unsupported_Media_Type_Response(Base_Response):
    code = HTTP_Status.UNSUPPORTED_MEDIA_TYPE
    error = True

    def __init__(self, exception=None, **kwargs):
        super().__init__(exception.title if exception is not None else 'Unsupported media type',
                         exception=exception, **kwargs)
