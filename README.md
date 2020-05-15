## Web app to bookmark links

<p align="center"><img align="center" src="bookmarks/static/img/logo_200x200.png"></p>

![Version](https://img.shields.io/badge/version-0.1.11-blue.svg?cacheSeconds=2592000)
[![License: GNU GPLv3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

### ✨ [Demo](https://pybook.evagelos.xyz)

## Install

```sh
pip install -e .
```

## Usage
Run in development environment
```sh
FLASK_ENV=development flask run
```
#### Use query string to filter and sort
* Bookmarks with _flask_ **and** _pyramid_ tags **and** sorted by oldest first `/bookmarks/?tag=flask&tag=pyramid&sort=-date`
* Bookmarks with _flask_ **or** _pyramid_ tags **and** sorted by highest rating first`/bookmarks/?tag=flask,pyramid&sort=rating`

## Run tests

```sh
pytest
```
## Resources

- [API Documentation](https://pybook.evagelos.xyz/api/v1/documentation)
- [Change log](CHANGELOG.md)

## Roadmap
### Done:
- [x] Sort bookmarks
- [x] Vote bookmarks (reddit style)
- [x] Tag bookmarks (reddit style)
- [x] Favourite bookmarks
- [x] Pagination
- [x] Auto-fetch link tile
- [x] Save link's image/favicon
- [x] User accounts
- [x] Subscribe to other users
- [x] API documentation (partially)

### Todo:
- [ ] Implement search functionality
- [ ] API documentation

## Author

* Website: https://evagelos.xyz
* Github: [@ev-agelos](https://github.com/ev-agelos)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!

Feel free to check [issues page](https://github.com/ev-agelos/PyBook/issues).

## Show your support

Give a ⭐️ if this project helped you!

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_

