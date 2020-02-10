from marshmallow import fields, Schema


class StatusResponseSchema(Schema):
    id = fields.String()
    agents = fields.List(fields.String())
    alive = fields.DateTime()
