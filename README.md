# Python-bookmarks
##### Flask app for saving Python related urls


Bookmark endpoints:

Get all bookmarks
```
/bookmarks/
```
Import bookmarks(Login required)
```
/bookmarks/import
```
Update bookmark by specifying title(Login required)
```
/bookmarks/title/update
```
Vote a bookmark
```
/bookmarks/title/vote
```

Category endpoints:

Get all categories
```
/categories
```
Get all bookmarks by specifying category name
```
/categories/name
```

Endpoints related to specific user:
Get all users
```
/users/
```
Get user by specifying username
```
/users/username
```
Get user's bookmarks by specifying username
```
/users/username/bookmarks/
```
Get user's bookmark by specofying username and bookmark title
```
/users/username/bookmarks/title
```
Get user's categories by specifying username
```
/users/username/categories
```
Get user's bookmarks by specifying username and category name
```
/users/username/categories/name
```

Auth endpoints:
```
/login
/logout (Login required)
/register
```
