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

### Endpoints:

`/bookmarks/` - Get all bookmarks
* `/bookmarks/?sort=date` - sort by newest
* `/bookmarks/?sort=-rating` - sort by lowest rating

`/bookmarks/<id>/update` - Update bookmark (login required)

`/bookmarks/<id>/vote` - Vote bookmark (login required)

`/bookmarks/<id>/delete` - Delete bookmark (login required)

`/bookmarks/<id>/save` - Save bookmark to favorites (login required)

`/bookmarks/add` - Add bookmark (login required)

`/bookmarks/import` - Import json file with bookmarks (login required)

`/bookmarks/search` - Search bookmarks (Not implemented yet)

`/categories/` - Get all categories

`/users/` - Get all users

`/users/<username>` - Get user's profile page

`/users/<username>/bookmarks/` - Get user's bookmarks

`/users/<username>/bookmarks/saved` - Get user's favorite bookmarks

`/users/activate/<token>` - Activate user's token(when registering new account)

`/login` - Login to website

`/logout` - Logout from website (Login required)

`/register` - Register to website
