from marshmallow import Schema
from marshmallow.fields import DateTime, Str
from utils.datetime import FORMAT


class StatusRequestSchema(Schema):
    """Response for status endpoint."""

    id = Str(required=True, example='apache',
             description='ID of the execution environment.')

    username = Str(allow_none=True,
                   description='Username for the CB to connect to this LCP.')

    password = Str(allow_none=True,
                   description='Password for the CB to connect to this LCP.')


class StatusResponseSchema(Schema):
    """Response for status endpoint."""

    id = Str(required=True, example='apache',
             description='ID of the execution environment.')

    started = DateTime(format=FORMAT, required=True, example='2019/02/14 15:23:30',
                       description='Timestamp when the LCP is started')

    last_heartbeat = DateTime(format=FORMAT, required=True, example='2019/02/14 15:23:33',
                              description='Timestamp of the expiration of the API access configuration.')

    username = Str(description='Username for the CB to connect to this LCP.')

    password = Str(description='Password for the CB to connect to this LCP.')
