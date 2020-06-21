from marshmallow.fields import DateTime as Date_Time, Str
from schema.base import Base_Schema
from utils.datetime import FORMAT

__all__ = [
    'Status_Request_Schema',
    'Status_Response_Schema'
]


class Status_Request_Schema(Base_Schema):
    """Response for status endpoint."""

    id = Str(required=True, example='apache',
             description='ID of the execution environment.')
    username = Str(allow_none=True,
                   description='Username for the CB to connect to this LCP.')
    password = Str(allow_none=True,
                   description='Password for the CB to connect to this LCP.')


class Status_Response_Schema(Base_Schema):
    """Response for status endpoint."""

    id = Str(required=True, example='apache',
             description='ID of the execution environment.')
    started = Date_Time(format=FORMAT, required=True, example='2019/02/14 15:23:30',
                        description='Timestamp when the LCP is started')
    last_heartbeat = Date_Time(format=FORMAT, required=True, example='2019/02/14 15:23:33',
                               description='Timestamp of the expiration of the API access configuration.')
    username = Str(description='Username for the CB to connect to this LCP.')
    password = Str(description='Password for the CB to connect to this LCP.')
