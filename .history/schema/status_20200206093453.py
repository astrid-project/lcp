class StatusResponseSchema(Schema):
    id = fields.String()
    agents = fields.List(fields.String())
    alive = fields.DateTime()

