"""Module for creating the Forms for the application."""

from marshmallow import validate

from bookmarks import ma
from bookmarks.models import Bookmark, Favourite, Vote, Tag
from bookmarks.users.models import User


class TagSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Tag
        fields = ('name', )


class BookmarkSchema(ma.SQLAlchemyAutoSchema):
    """Bookmark representation."""

    class Meta:
        model = Bookmark

    tags = ma.Nested(TagSchema, many=True)


class BookmarksQueryArgsSchema(ma.Schema):
    """Query string parameters for getting bookmarks."""

    tag = ma.List(ma.String(), missing=[], allow_none=True)
    sort = ma.String(
        validate=validate.OneOf(['date', '-date', 'rating', '-rating']),
        missing='date'
    )


class BookmarkPOSTSchema(ma.SQLAlchemySchema):
    """Request arguments for creating a new bookmark."""

    title = ma.String(required=True, validate=validate.Length(min=10))
    url = ma.URL(required=True, schemes=('http', 'https'))
    tags = ma.List(ma.String(validate=validate.Length(min=3)), missing=['uncategorized'])


class BookmarkPUTSchema(ma.SQLAlchemySchema):
    """Request arguments for updating an existing bookmark."""

    title = ma.String(required=True, validate=validate.Length(min=10))
    url = ma.URL(required=True, schemes=('http', 'https'))
    tags = ma.List(ma.String())


class FavouriteSchema(ma.SQLAlchemyAutoSchema):
    """Favourite representation."""

    class Meta:
        model = Favourite


class FavouritePOSTSchema(ma.SQLAlchemySchema):
    """Request arguments for adding a new bookmark to favourites."""

    class Meta:
        model = Favourite

    bookmark_id = ma.auto_field()


class VoteSchema(ma.SQLAlchemyAutoSchema):
    """Vote representation."""

    class Meta:
        model = Vote

class VotePOSTSchema(ma.SQLAlchemyAutoSchema):
    """Request arguments for adding new vote."""

    class Meta:
        model = Vote

    bookmark_id = ma.auto_field()
    direction = ma.Int(validate=validate.OneOf([-1, 1]))


class UserSchema(ma.SQLAlchemyAutoSchema):
    """User representation."""

    class Meta:
        model = User
