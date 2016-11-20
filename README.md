[![build status](https://gitlab.com/evagelos/PyBook/badges/master/build.svg)](https://gitlab.com/evagelos/PyBook/commits/master) [![codecov](https://codecov.io/gl/evagelos/PyBook/branch/master/graph/badge.svg?token=w1Ca3TbhhS)](https://codecov.io/gl/evagelos/PyBook) [![Dependency Status](https://gemnasium.com/badges/289695fd0eeecc1e035b5e1618850179.svg)](https://gemnasium.com/323e5f4a737906309571417eed57b761) [![Documentation Status](https://readthedocs.org/projects/python-bookmarks/badge/?version=latest)](http://python-bookmarks.readthedocs.org/en/latest/?badge=latest)
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
