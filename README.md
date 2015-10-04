# Python-bookmarks
##### Flask app for saving Python related urls


Bookmark endpoints:
- /bookmarks
- /bookmarks/title/vote
- /bookmarks/import *(Login required)*

Category endpoints:
- /categories
- /categories/name

Auth endpoints:
- /login
- /logout *(Login required)*
- /register

Endpoints related to specific user:
- /users/
- /users/username
- /users/username/bookmarks/
- /users/username/bookmarks/title
- /users/username/bookmarks/title/update *(Login required)*
- /users/username/bookmarks/add *(Login required)*
- /users/username/categories
- /users/username/categories/name
