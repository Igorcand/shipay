from marshmallow import Schema, fields, validate


class CreateClaimInputSchema(Schema):
    description = fields.Str(required=False, validate=validate.Length(min=1, max=255))
    active = fields.Bool(missing=False)

class CreateClaimOutputSchema(Schema):
    id = fields.UUID()

class ClaimOutputSchema(Schema):
    id = fields.UUID(required=True)  # Campo UUID
    description = fields.Str(required=True, validate=validate.Length(max=255))  # Campo String com validação de comprimento
    active = fields.Bool(missing=False)

class ListClaimOutputSchema(Schema):
    data = fields.List(fields.Nested(ClaimOutputSchema))  # Lista de LinkResponseSchema

class UpdateClaimInputSchema(Schema):
    description = fields.Str(missing=None, validate=validate.Length(min=0, max=255))
    active = fields.Bool(missing=False)
