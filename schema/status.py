from marshmallow import fields, Schema


class StatusResponseSchema(Schema):
    id = fields.String(required=True, description='ID of the execution environment.',
                       example='fa7ca1b7-80b5-4a47-8cc6-2cb1ca0ed778')
    agent = fields.List(fields.String(required=True,
                        description='ID of the agent instances installed in this execution environment.',
                        example='agent-filebeat-1'))
    started = fields.DateTime(description='Timestamp when the LCP is started in this execution environment',
                              example='2019_02_14-15:23:30')
