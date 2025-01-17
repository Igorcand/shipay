from marshmallow import Schema, fields, validate


class CreateUserInputSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    email = fields.Str(required=True, validate=validate.Email())
    role_id = fields.UUID(required=True)
    password = fields.Str(load_default=None, allow_none=True)


class CreateUserOutputSchema(Schema):
    id = fields.UUID()

class UserOutputSchema(Schema):
    id = fields.UUID(required=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    email = fields.Str(required=True, validate=validate.Email())
    role_id = fields.UUID(required=True)

class GetUserOutputSchema(Schema):
    id = fields.UUID(required=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    email = fields.Str(required=True, validate=validate.Email())
    role = fields.Str(required=True, validate=validate.Length(max=255))

class ListUserOutputSchema(Schema):
    data = fields.List(fields.Nested(UserOutputSchema))  # Lista de LinkResponseSchema

class UpdateUserInputSchema(Schema):
    email = fields.Str(load_default=None, validate=validate.Email())
    password = fields.Str(load_default=None, allow_none=True)
