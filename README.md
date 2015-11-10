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

/bookmarks/ endpoints:

`/bookmarks/` (Get all bookmarks)

```
/bookmarks/<title>/update (Update bookmark by specifying title, login required)
/bookmarks/<title>/vote (Vote a bookmark according to <title>, login required)

/bookmarks/categories (Get all categories)
/bookmarks/categories/<name> (Get bookmarks by category <name>)

/bookmarks/import (Import bookmarks, login required)
```

/categories/ endpoints:

```
/categories (Get all categories)
/categories/name (Get all bookmarks by specifying category name)
```

/users/ enpoints

```
/users/ (Get all users)
/users/<username> (Get user profile according to <username>)

/users/<username>/bookmarks/ (Get user's bookmarks according to <username>)
/users/<username>/bookmarks/<title> (Get user's bookmark according to <username> and bookmark <title>)

/users/<username>/bookmarks/add (Add a new bookmark, login required)

/users/<username>/categories (Get user's categories by specifying username)
/users/<username>/categories/<name> (Get user's bookmarks by specifying username and category name)
```

Auth endpoints:
```
/login
/logout (Login required)
/register
```
