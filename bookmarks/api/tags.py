from flask.views import MethodView
from flask_smorest import Blueprint
from sqlalchemy import func

from bookmarks import csrf, db
from bookmarks.models import Tag, tags_bookmarks

from .schemas import TagsSchema

tags_api = Blueprint('tags_api', 'Tags', url_prefix='/api/v1/tags/',
                     description='Operations on Tags')


@tags_api.route('/')
class TagsAPI(MethodView):

    decorators = [csrf.exempt]

    @tags_api.response(TagsSchema(many=True))
    def get(self):
        """Return all tags."""
        temp =  db.session.query(Tag.name, func.count(Tag.id).label('count')).join(
            tags_bookmarks).group_by(Tag.id).all()
        return temp
