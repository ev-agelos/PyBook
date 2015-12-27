"""Schemas for creating JSON results."""


from marshmallow import Schema, fields


class UserSchema(Schema):
    """Schema for User model."""

    username = fields.String()
    email = fields.String()
    created_on = fields.DateTime()
    updated_on = fields.DateTime()


class CategorySchema(Schema):
    """Schema for Category model."""

    name = fields.String()


class BookmarkSchema(Schema):
    """Schema for Bookmark model."""

    _id = fields.Integer()
    title = fields.String()
    url = fields.String()
    rating = fields.Integer()
    created_on = fields.DateTime(format='%d/%m/%Y - %H:%M')
    updated_on = fields.DateTime(format='%d/%m/%Y - %H:%M')
    thumbnail = fields.String()

    user_id = fields.Integer()
    category_id = fields.Integer()


class VoteSchema(Schema):
    """Schema for Vote model."""
    
    direction = fields.Boolean()
    user_id = fields.Integer()
    bookmark_id = fields.Integer()


class SaveBookmarkSchema(Schema):
    """Schema for SaveBookmark model."""

    saved_on = fields.DateTime(format='%d/%m/%Y - %H:%M')
    user_id = fields.Integer()
    bookmark_id = fields.Integer()
