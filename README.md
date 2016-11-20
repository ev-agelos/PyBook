[![Build Status](https://travis-ci.org/ev-agelos/Python-bookmarks.svg?branch=master)](https://travis-ci.org/ev-agelos/Python-bookmarks) [![Coverage Status](https://coveralls.io/repos/ev-agelos/Python-bookmarks/badge.svg?branch=master&service=github)](https://coveralls.io/github/ev-agelos/Python-bookmarks?branch=master) [![Requirements Status](https://requires.io/github/ev-agelos/Python-bookmarks/requirements.svg?branch=master)](https://requires.io/github/ev-agelos/Python-bookmarks/requirements/?branch=master) [![Documentation Status](https://readthedocs.org/projects/python-bookmarks/badge/?version=latest)](http://python-bookmarks.readthedocs.org/en/latest/?badge=latest)
# PyBook
Flask app for keeping all python related links in one place.

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

#### Sorting by date or rating:
getting newest first `/bookmarks/?sort=date` or getting lowest rating first `/bookmarks/?sort=-rating`

#### Filtering by category:
`/bookmarks/?category=tutorials`

### Endpoints:
`/api/auth/request-token` POST

`/api/bookmarks/` GET, POST

`/api/bookmarks/<int:bookmark_id>/votes` GET

`/api/bookmarks/<int:id>` GET, PUT, DELETE

`/api/save` POST

`/api/unsave` DELETE

`/api/vote` POST, PUT, DELETE

`/api/users/` GET

`/api/users/<int:id>` GET, PUT, DELETE

`/api/users/<int:id>/favourites` GET

`/api/users/<int:id>/votes` GET
