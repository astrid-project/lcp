from marshmallow import fields, Schema


class CodeRequestSchema(Schema):
    name = fields.String(required=True)
    source = fields.String(required=True)


class ResultResponseSchema(Schema):
    warning = fields.String()


class InjectedResponseSchema(ResultResponseSchema):
    name = fields.String(required=True)
    injected = fields.Boolean(required=True)


class ErrorResponseSchema(ResultResponseSchema):
    error = fields.Boolean(required=True)
    description = fields.String(required=True)


class CodeResponseSchema(Schema):
    when = fields.DateTime(required=True)
    results = fields.List(fields.Nested(ResultResponseSchema()), required=True)
