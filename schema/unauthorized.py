from marshmallow import fields, Schema

class UnauthorizedSchema(Schema):
   """
   Unauthorized operation.
   """
   title = fields.String(required=True, enum=["401 Unauthorized"], description="Title error", example="401 Unauthorized")
   description = fields.String(required=True, enum=["Invalid Username/Password."],
                               description="Human readable message that describes the error.",
                               example="Invalid Username/Password.")
