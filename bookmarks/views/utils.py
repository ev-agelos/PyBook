"""Helper methods."""

from flask import request


def paginate(query):
    """Return a query result paginated."""
    return query.paginate(page=request.args.get('page', 1), per_page=5)
