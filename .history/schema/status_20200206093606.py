from marshmallow import fields, Schema


class StatusRequestSchema(Schema):
    pass


class StatusResponseSchema(Schema):
    id = fields.String()
    alive = fields.DateTime()
