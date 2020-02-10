from marshmallow import fields, Schema


class StatusResponseSchema(Schema):
    id = fields.String()
    alive = fields.DateTime()
