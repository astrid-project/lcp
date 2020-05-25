from marshmallow import Schema
from marshmallow.fields import DateTime, String


class StatusResponseSchema(Schema):
    id = String(required=True, description='ID of the execution environment.', example='apache')
    started = DateTime(required=True, description='Timestamp when the LCP is started',
                       example='2019_02_14 15:23:30')
    last_heartbeat = DateTime(required=True,
                              description='Timestamp of the last hearthbeat between the LCP and the CB',
                              example='2019_02_14 15:23:33')
