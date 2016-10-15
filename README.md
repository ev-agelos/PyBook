[![Build Status](https://travis-ci.org/ev-agelos/Python-bookmarks.svg?branch=master)](https://travis-ci.org/ev-agelos/Python-bookmarks) [![Coverage Status](https://coveralls.io/repos/ev-agelos/Python-bookmarks/badge.svg?branch=master&service=github)](https://coveralls.io/github/ev-agelos/Python-bookmarks?branch=master) [![Requirements Status](https://requires.io/github/ev-agelos/Python-bookmarks/requirements.svg?branch=master)](https://requires.io/github/ev-agelos/Python-bookmarks/requirements/?branch=master) [![Documentation Status](https://readthedocs.org/projects/python-bookmarks/badge/?version=latest)](http://python-bookmarks.readthedocs.org/en/latest/?badge=latest)
# Python-bookmarks
Flask app for keeping all python related links in one place.

Reason for creating this app was firstly keeping all Python(and not only) goodies that exist on internet,
and secondly Flask is FUN! :D

App is hosted on [PythonAnywhere](http://evagelos.pythonanywhere.com/)!

### Done:
- [x] Import multiple bookmarks(json file)
- [x] Order bookmarks by new/old/top/unpopular
- [x] Voting bookmarks(reddit style)
- [x] Page navigation
- [x] Add 'suggest title' when user adds new bookmark
- [x] When adding new bookmark, save the favicon/image of the link
- [x] Add verification/confirmation when new user registers
- [x] Ability to save bookmarks(favourites)

### Todo:
- [ ] Implement search functionality
- [ ] User profile page
- [ ] Better error responses
- [ ] Forgot password

### Tips:
Bookmarks can be sorted by appending request arguments,
sorting by newest: `/bookmarks/?sort=date` or
sorting by lowest rating: `/bookmarks/?sort=-rating`

### Endpoints:
GET `/bookmarks/` - Get all bookmarks
GET `/bookmarks/<id>` - Get bookmark identified by id

GET `/bookmarks/add` - Get the form to add new bookmark
POST `/bookmarks/` - Add new bookmark

GET `/bookmarks/<id>/update` - Get the form to update a bookmark
PUT `/bookmarks/<id>` - Update bookmark identified by id

DELETE `/bookmarks/<id>` - Delete bookmark identified by id

PUT `/bookmarks/<id>/save` - Save bookmark identified by id

POST `/bookmarks/<id>/vote` - Vote bookmark identified by id

GET/POST `/bookmarks/import` - Get/Post form to import bookmarks in json (login required)

GET `/bookmarks/search` - Get form to search bookmarks (Not implemented yet)

GET `/categories/` - Get all categories

GET `/users/` - Get all users

GET `/users/<username>` - Get user's profile page

GET `/users/<username>/bookmarks/` - Get user's bookmarks

GET `/users/<username>/bookmarks/saved` - Get user's favorite bookmarks

GET `/users/activate/<token>` - Activate user's token(when registering new account)

GET/POST `/login` - Login to PyBookmarks

GET `/logout` - Logout from website (Login required)

GET/POST `/register` - Register to website
