from marshmallow import Schema, fields, validate


class CreateRoleInputSchema(Schema):
    description = fields.Str(required=True, validate=validate.Length(min=1, max=255))


class CreateRoleOutputSchema(Schema):
    id = fields.UUID()

class RoleOutputSchema(Schema):
    id = fields.UUID(required=True)  # Campo UUID
    description = fields.Str(required=True, validate=validate.Length(max=255))  # Campo String com validação de comprimento

class ListRoleOutputSchema(Schema):
    data = fields.List(fields.Nested(RoleOutputSchema))  # Lista de LinkResponseSchema

class UpdateRoleInputSchema(Schema):
    description = fields.Str(required=True, validate=validate.Length(min=1, max=255))
