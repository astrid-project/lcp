from marshmallow import Schema
from marshmallow.fields import DateTime, Nested
from schema.code.response.result import CodeResultResponseSchema


class CodeResponseSchema(Schema):
   """
   Response for code endpoint.
   """
   when = DateTime(required=True, description='Datetime of the configuration changes.',
                   example='2020/02/13 15:27:06')
   results = Nested(CodeResultResponseSchema, many=True, required=True)
