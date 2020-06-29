from lib.response import *
from marshmallow import Schema, validate
from marshmallow.fields import Bool, Constant, Integer, Nested, Str


__all__ = [
    'Bad_Request_Response_Schema',
    'Conflict_Response_Schema',
    'Content_Response_Schema',
    'Created_Response_Schema',
    'No_Content_Response_Schema',
    'Not_Acceptable_Response_Schema',
    'Not_Found_Response_Schema',
    'Not_Modified_Response_Schema',
    'Ok_Response_Schema',
    'Reset_Content_Response_Schema',
    'Unauthorized_Response_Schema',
    'Unprocessable_Entity_Response_Schema',
    'Unsupported_Media_Type_Response_Schema'
]

RESPONSE_STATUS = [
    Bad_Request_Response.status(),
    Conflict_Response.status(),
    Content_Response.status(),
    Created_Response.status(),
    No_Content_Response.status(),
    Not_Acceptable_Response.status(),
    Not_Found_Response.status(),
    Not_Modified_Response.status(),
    Ok_Response.status(),
    Reset_Content_Response.status(),
    Unauthorized_Response.status(),
    Unprocessable_Entity_Response.status(),
    Unsupported_Media_Type_Response.status()
]

RESPONSE_CODES = [
    Bad_Request_Response.code,
    Conflict_Response.code,
    Content_Response.code,
    Created_Response.code,
    No_Content_Response.code,
    Not_Acceptable_Response.code,
    Not_Found_Response.code,
    Not_Modified_Response.code,
    Ok_Response.code,
    Reset_Content_Response.code,
    Unauthorized_Response.code,
    Unprocessable_Entity_Response.code,
    Unsupported_Media_Type_Response.code
]


class Exception_Response_Schema(Schema):
    reason = Str(required=True, example='Connection timeout',
                 description='Exception reason.')
    filename = Str(required=True, example='lib/connection.py',
                   description='Filename where the exception is raised.')
    line = Integer(required=True, example=80,
                   description='Line where the exception is raised.')


class Base_Response_Schema(Schema):
    """Response for the item creation."""

    status = Str(required=True, enum=RESPONSE_STATUS,
                 example=RESPONSE_STATUS[0],
                 description='HTTP Status Code phrase.',
                 validate=validate.OneOf(RESPONSE_STATUS))
    error = Bool(default=False, example=False,
                 description='Indicate the presence of an error')
    message = Str(required=True, example='Request not valid: two ids provided.',
                  description='Human readable message that describes the status of the operation.')
    exception = Nested(Exception_Response_Schema,
                       description='Message of the occurred exception.')
    code = Integer(required=True, enum=RESPONSE_CODES,
                   example=RESPONSE_CODES[0],
                   description='HTTP Status Code.',
                   validate=validate.OneOf(RESPONSE_CODES))


class Bad_Request_Response_Schema(Base_Response_Schema):
    status = Constant(constant=Bad_Request_Response.status())
    error = Constant(constant=Bad_Request_Response.error)
    code = Constant(constant=Bad_Request_Response.code)


class Conflict_Response_Schema(Base_Response_Schema):
    status = Constant(constant=Conflict_Response.status())
    error = Constant(constant=Conflict_Response.error)
    code = Constant(constant=Conflict_Response.code)


class Created_Response_Schema(Base_Response_Schema):
    status = Constant(Created_Response.status())
    error = Constant(Created_Response.error)
    code = Constant(Created_Response.code)


class Internal_Server_Error_Response_Schema(Base_Response_Schema):
    status = Constant(Internal_Server_Error_Response.status())
    error = Constant(Internal_Server_Error_Response.error)
    code = Constant(Internal_Server_Error_Response.code)


class No_Content_Response_Schema(Base_Response_Schema):
    status = Constant(No_Content_Response.status())
    error = Constant(No_Content_Response.error)
    code = Constant(No_Content_Response.code)


class Not_Acceptable_Response_Schema(Base_Response_Schema):
    status = Constant(Not_Acceptable_Response.status())
    error = Constant(Not_Acceptable_Response.error)
    code = Constant(Not_Acceptable_Response.code)


class Not_Found_Response_Schema(Base_Response_Schema):
    status = Constant(Not_Found_Response.status())
    error = Constant(Not_Found_Response.error)
    code = Constant(Not_Found_Response.code)


class Not_Modified_Response_Schema(Base_Response_Schema):
    status = Constant(Not_Modified_Response.status())
    error = Constant(Not_Modified_Response.error)
    code = Constant(Not_Modified_Response.code)


class Ok_Response_Schema(Base_Response_Schema):
    status = Constant(Ok_Response.status())
    error = Constant(Ok_Response.error)
    code = Constant(Ok_Response.code)


class Content_Response_Schema(Ok_Response_Schema):
    status = Constant(Content_Response.status())
    error = Constant(Content_Response.error)
    code = Constant(Content_Response.code)


class Reset_Content_Response_Schema(Base_Response_Schema):
    status = Constant(Reset_Content_Response.status())
    error = Constant(Reset_Content_Response.error)
    code = Constant(Reset_Content_Response.code)


class Unauthorized_Response_Schema(Base_Response_Schema):
    status = Constant(Unauthorized_Response.status())
    error = Constant(Unauthorized_Response.error)
    code = Constant(Unauthorized_Response.code)


class Unprocessable_Entity_Response_Schema(Base_Response_Schema):
    status = Constant(Unprocessable_Entity_Response.status())
    error = Constant(Unprocessable_Entity_Response.error)
    code = Constant(Unprocessable_Entity_Response.code)


class Unsupported_Media_Type_Response_Schema(Base_Response_Schema):
    status = Constant(Unsupported_Media_Type_Response.status())
    error = Constant(Unsupported_Media_Type_Response.error)
    code = Constant(Unsupported_Media_Type_Response.code)
