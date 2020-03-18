[![build status](https://gitlab.com/evagelos/PyBook/badges/master/build.svg)](https://gitlab.com/evagelos/PyBook/commits/master) [![codecov](https://codecov.io/gl/evagelos/PyBook/branch/master/graph/badge.svg?token=w1Ca3TbhhS)](https://codecov.io/gl/evagelos/PyBook)
# PyBook
App for saving python related links.


### Done:
- [x] Able to order bookmarks
- [x] Able to vote bookmarks (reddit style)
- [x] Bookmarks navigation
- [x] Button to auto-fetch bookmark's tile
- [x] Save related image of bookmark
- [x] User accounts
- [x] Able to favourite bookmarks

### Todo:
- [ ] Implement search functionality
- [ ] API documentation

#### Sorting by date or rating:
getting newest first `/bookmarks/?sort=date` or getting lowest rating first `/bookmarks/?sort=-rating`

#### Filtering by tag:
* get bookmarks with _flask_ **and** _pyramid_ tags `/bookmarks/?tag=flask&tag=pyramid`
* get bookmarks with _flask_ **or** _pyramid_ tags `/bookmarks/?tag=flask,pyramid`
