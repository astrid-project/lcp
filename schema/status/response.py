from marshmallow import Schema
from marshmallow.fields import DateTime, Str


class StatusResponseSchema(Schema):
    """Response for status endpoint."""
    id = Str(required=True, description='ID of the execution environment.', example='apache')
    started = DateTime(required=True, description='Timestamp when the LCP is started',
                       example='2019_02_14 15:23:30')
    last_heartbeat = DateTime(required=True, example='2019_02_14 15:23:33',
                              description='Timestamp of the last hearthbeat between the LCP and the CB')
