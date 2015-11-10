# Python-bookmarks
Flask app for keeping all python related links in one place.

Reason for creating this app was firstly keeping all Python(and not only) goodies that exist on internet,
and secondly Flask is FUN! :D

App is hosted on [PythonAnywhere](http://evagelos.pythonanywhere.com/)!

## Features:
- [x] Import multiple bookmarks(json file)
- [x] Order bookmarks by new/old/top/unpopular
- [x] Voting bookmarks(reddit style)
- [x] Page navigation

## TODO:
- [ ] Send email confirmation when user registers
- [ ] Add 'suggest title' when user adds new bookmark
- [ ] Add option for users to add(or save) bookmarks from other users
- [ ] When adding new bookmark, save the favicon/image of the link
- [ ] Implement search functionality
- [ ] User profile page

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

`/login` - Login to website

`/logout` - Logout from website (Login required)

`/register` - Register to website
