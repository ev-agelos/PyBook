# Python-bookmarks
##### Flask app for saving Python related urls


Bookmark endpoints:

```
/bookmarks/ (Get all bookmarks)
/bookmarks/import (Import bookmarks(Login required))
/bookmarks/title/update (Update bookmark by specifying title(Login required))
/bookmarks/title/vote (Vote a bookmark)
```

Category endpoints:

```
/categories (Get all categories)
/categories/name (Get all bookmarks by specifying category name)
```

Endpoints related to specific user:

```
/users/ (Get all users)
/users/username (Get user by specifying username)
/users/username/bookmarks/ (Get user's bookmarks by specifying username)
/users/username/bookmarks/title (Get user's bookmark by specofying username and bookmark title)
/users/username/categories (Get user's categories by specifying username)
/users/username/categories/name (Get user's bookmarks by specifying username and category name)
```

Auth endpoints:
```
/login
/logout (Login required)
/register
```
