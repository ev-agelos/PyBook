[![Build Status](https://travis-ci.org/ev-agelos/Python-bookmarks.svg?branch=master)](https://travis-ci.org/ev-agelos/Python-bookmarks) [![Coverage Status](https://coveralls.io/repos/ev-agelos/Python-bookmarks/badge.svg?branch=master&service=github)](https://coveralls.io/github/ev-agelos/Python-bookmarks?branch=master) [![Requirements Status](https://requires.io/github/ev-agelos/Python-bookmarks/requirements.svg?branch=master)](https://requires.io/github/ev-agelos/Python-bookmarks/requirements/?branch=master) [![Documentation Status](https://readthedocs.org/projects/python-bookmarks/badge/?version=latest)](http://python-bookmarks.readthedocs.org/en/latest/?badge=latest)
# Python-bookmarks
Flask app for keeping all python related links in one place.

Reason for creating this app was firstly keeping all Python(and not only) goodies that exist on internet,
and secondly Flask is FUN! :D

App is hosted on [PythonAnywhere](http://evagelos.pythonanywhere.com/)!

## Done:
- [x] Import multiple bookmarks(json file)
- [x] Order bookmarks by new/old/top/unpopular
- [x] Voting bookmarks(reddit style)
- [x] Page navigation
- [x] Add 'suggest title' when user adds new bookmark
- [x] When adding new bookmark, save the favicon/image of the link
- [x] Add verification/confirmation when new user registers

## Todo:
- [ ] Add option for users to add(or save) bookmarks from other users and maybe subscribe to them
- [ ] Implement search functionality
- [ ] User profile page
- [ ] Better error responses
- [ ] Forgot password

## ENDPOINTS:

`/bookmarks/` - Get all bookmarks

`/bookmarks/<title>/update` - Update bookmark (login required)

`/bookmarks/<title>/vote` - Vote bookmark (login required)

`/bookmarks/categories` - Get all categories

`/bookmarks/categories/<name>` - Get bookmarks by category

`/bookmarks/import` - Import json file with bookmarks (login required)

`/categories` - Get all categories

`/categories/<name>` - Get all bookmarks by category

`/users/` - Get all users

`/users/<username>` - Get user's profile page

`/users/<username>/bookmarks/` - Get user's bookmarks

`/users/<username>/bookmarks/<title>` - Get user's specific bookmark

`/users/<username>/bookmarks/add` - Add a new bookmark (login required)

`/users/<username>/categories` - Get user's categories

`/users/<username>/categories/<name>` - Get user's bookmarks by category

`/users/activate/<token>` - Activate user given valid token

`/login` - Login to website

`/logout` - Logout from website (Login required)

`/register` - Register to website
