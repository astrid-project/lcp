from marshmallow import fields, Schema


class StatusResponseSchema(Schema):
    id = fields.String(required=True, description='ID of the execution environment.',
                       example='fa7ca1b7-80b5-4a47-8cc6-2cb1ca0ed778')
    started = fields.DateTime(required=True, description='Timestamp when the LCP is started in this execution environment',
                              example='2019_02_14-15:23:30')
    last_heartbeat = fields.DateTime(required=True,
                                     description='Timestamp of the last hearthbeat between the LCP and the CB',
                                     example='2019_02_14-15:23:33')
