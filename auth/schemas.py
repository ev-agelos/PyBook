"""Schemas for auth package."""


from marshmallow import Schema, fields


class UserSchema(Schema):
    """Schema for User model."""

    username = fields.String()
    email = fields.String()
    created_on = fields.DateTime()
    updated_on = fields.DateTime()
