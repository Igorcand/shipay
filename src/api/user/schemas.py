from marshmallow import Schema, fields, validate


class CreateUserInputSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    email = fields.Str(required=True, validate=validate.Email())
    role_id = fields.UUID(required=True)
    password = fields.Str(missing=None, allow_none=True)


class CreateUserOutputSchema(Schema):
    id = fields.UUID()

class UserOutputSchema(Schema):
    id = fields.UUID(required=True)  # Campo UUID
    name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    email = fields.Str(required=True, validate=validate.Email())
    role_id = fields.UUID(required=True)

class ListUserOutputSchema(Schema):
    data = fields.List(fields.Nested(UserOutputSchema))  # Lista de LinkResponseSchema

class UpdateUserInputSchema(Schema):
    email = fields.Str(missing=None, validate=validate.Email())
    password = fields.Str(missing=None, allow_none=True)
