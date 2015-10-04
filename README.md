# Python-bookmarks
##### Flask app for saving Python related urls


Bookmark endpoints:
- /bookmarks
- /bookmarks/bookmark_id/vote
- /bookmarks/import ######*Login required*

Category endpoints:
- /categories
- /categories/category_id

Auth endpoints:
- /login
- /logout ######*Login required*
- /register

Endpoints related to specific user:
- /users/
- /users/user_id
- /users/user_id/bookmarks/
- /users/user_id/bookmarks/bookmark_id
- /users/user_id/bookmarks/bookmark_id/update ######*Login required*
- /users/user_id/bookmarks/add ######*Login required*
- /users/user_id/categories
- /users/user_id/categories/category_id
