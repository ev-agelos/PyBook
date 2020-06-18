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

    user_id = ma.Int()
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
    """Request arguments for creating a new bookmark."""

    title = ma.String(validate=validate.Length(min=10))
    url = ma.URL(schemes=('http', 'https'))
    tags = ma.List(ma.String(validate=validate.Length(min=3)))


class FavouriteSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Favourite

    bookmark = ma.HyperlinkRelated('bookmarks_api.BookmarkAPI', id='<id>')


class FavouritePOSTSchema(ma.SQLAlchemySchema):
    """Request arguments for adding a new bookmark to favourites."""

    class Meta:
        model = Favourite

    bookmark_id = ma.auto_field()


class VoteSchema(ma.SQLAlchemyAutoSchema):
    """Vote representation."""

    class Meta:
        model = Vote
        include_fk = True


class VotePOSTSchema(ma.SQLAlchemyAutoSchema):
    """Request arguments for adding new vote."""

    class Meta:
        model = Vote

    bookmark_id = ma.auto_field()
    direction = ma.Int(required=True, validate=validate.OneOf([-1, 1]))


class VotePUTSchema(ma.SQLAlchemyAutoSchema):
    """Request arguments for updating a vote."""

    class Meta:
        model = Vote
        fields = ('direction', )

    direction = ma.Int(required=True, validate=validate.OneOf([-1, 1]))


class SubscriptionsSchema(ma.ModelSchema):

    class Meta:
        model = User
        fields = ('user', )

    user = ma.UrlFor('users_api.UserAPI', id='<id>', _external=False)


class SubscriptionsGETSchema(ma.Schema):
    """Request arguments in query string."""

    mySubscribers = ma.Boolean(missing=False)


class SubscriptionsPOSTSchema(ma.Schema):

    user_id = ma.Int(required=True)


class UserPUTSchema(ma.Schema):

    username = ma.Str()
    email = ma.Email()
    currentPassword = ma.Str()
    newPassword = ma.Str()
    confirmPassword = ma.Str()
