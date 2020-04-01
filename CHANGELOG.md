
0.1.8 / 2020-04-01
==================

  * Bump version: 0.1.7 → 0.1.8
  * show logs when running via gunicorn
  * don't fetch image if cloudinary isn't set
  * do not set celery for testing
  * fix checking for production environment

0.1.7 / 2020-03-31
==================

  * Bump version: 0.1.6 → 0.1.7
  * fix setting production secret key

0.1.6 / 2020-03-31
==================

  * Bump version: 0.1.5 → 0.1.6
  * start using bump2version
  * add production configuration, simplified setting configuration

0.1.5 / 2020-03-30
==================

  * prepare release 0.1.5
  * use celery to send emails
  * no need to login to registry to pull the image
  * update readme
  * fix badge url
  * use multistage build, revert back to alpine

0.1.4 / 2020-03-20
==================

  * track all files in migrations directory

0.1.3 / 2020-03-20
==================

  * fix registering event listeners, use ajax for all requests
  * refactor tests
  * fix redirecting to profile page after updating it
  * use --password-stdin when logging with docker
  * suppress warning for Flask-Sqlalchemy event system
  * fix ignoring migrations when building docker image

0.1.2 / 2020-03-19
==================

  * use a common config class, allow migrate in all environments
  * bump version to 0.1.2
  * add rel="noopener noreferrer" in links with target=_blank
  * fix removing any inline javascript
  * fix having unique field ids for CSRF in forms
  * fix modal size
  * update README
  * add swagger for bookmarks, move API under /api/v1/
  * fix using CSRF with Ajax requests
  * start tracking migrations, update gitignore
  * fix recaptcha for dev config
  * use Flask pluggable views, extend API

0.1.1 / 2020-03-13
==================

  * improve configuration handling
  * Update LICENSE
  * build & deploy on 'Release' keyword
  * add changelog
  * build & deploy only on master with the keyword 'release' but uppercase

v0.1 / 2020-03-10
=================

  * fix warning
  * bump flask-sqlalchemy to 2.4.1
  * remove sphinx docs
  * replace alpine with debian (buster)
  * use alpine docker image
  * build image and release on new tag only
  * update sending coverage report to codecov
  * fix csrf when deleting bookmark and voting
  * fix bug when updating/deleting vote
  * try to find url's logo, improve scraping the favicon
  * migrate to new sentry-sdk
  * bump up libraries, fix warnings
  * update ssh commands for deployment
  * use host from request instead of env variable
  * fix signup url in template
  * change email service
  * include SAST in gitlab ci
  * pytest must be after any pytest-<plugin name> in requirements
  * add gitlab dependency scanning ci job
  * use stdin for docker password
  * support python3.8
  * smoke test from .gitlab-ci.yml
  * redirect to bookmarks on root path, support latest werkzeug
  * fix author email
  * remove sqlalchemy pin from dev requirements
  * bump Flask-WTF to 0.13.1
  * bump flask to 1.0.2
  * bump flask-marshmallow to 0.9.0, bump marshmallow-sqlalchemy to 0.15.0
  * bump flask to 0.12.4, bump python to 3.7
  * use env variable for server url
  * use variable for the website url as it might change
  * fix wrong setter name
  * dont pin requests,raven, rm opbeat service
  * update using sparkpost for emailing
  * fix url
  * pin sqlalclemy to 0.9.7 cause hybrid property error, update pytest deprecated ini setting
  * remove gemnasium badge
  * add plugin to run tests in parallel
  * update jquery version to 3.2.1
  * fix false triggering of login animation
  * Fix passing events in event listener functions
  * fix dynamic url creation for subscriptions
  * category and select category form fields dont exist anymore
  * replace variables to use gitlab's
  * reverted back to bind to 0.0.0.0
  * bind app to localhost
  * disable/re-enable suggest button when adding/updating bookmark to give feedback, closes #10
  * run ci tests in parallel
  * support multiple tag filtering, closes #18
  * run tests with pytest-xdist plugin
  * recaptcha needs config options at least empty for testing
  * include previous request args when sorting
  * save the https version of uploaded image
  * updated link, 2017 copyright
  * flask-wtf already includes reCaptcha
  * removed importing functionality
  * added tagging functionality and removed categorizing
  * removed uncalled jinja block
  * fixed unintented bug
  * use cloudinary for hosting images
  * removed unnecessary argument
  * read requirements form setup.py
  * fixed /search response
  * added (missing)tests for subscriptions API
  * added tests for users API
  * fixed Location header
  * fixed assertion on response headers
  * fixed response message
  * user HyperlinkRelated for user url in SubscriptionsSchema
  * fixed schema for favourites table
  * added SERVER_NAME to config for testing
  * updated docstring
  * delete user's favourites when deleting user
  * added tests for votes API
  * always g.user.id will own the vote
  * fixed argument name
  * bookmark_id must be an int
  * get POST args safer
  * added tests
  * file renaming
  * added tests, small refactoring
  * decouple request code from queries
  * ignore .egg-info and docs build generated folders
  * added tests
  * moved (un)save API endpoints to bookmarks
  * use db from conftest while in the request
  * added setup.py, removed __init__ from tests as PyTest recommends
  * added tests
  * save user to g after verifying his token in a API request
  * make bookmarks.views.utils file monkey-patchable by pytest
  * monkeypatch downloading bookmark's image
  * added tests
  * updated flask, use scoped session per test(wrapping each test to a transaction/rollback)
  * Merge branch 'feature-parallel-image-download' into 'master'
  * download url's image in parallel, download favicon if no og:image was found
  * return empty title if no response
  * renamed a template string
  * renamed app folder for docker, try to create db every time app starts
  * renamed database
  * removed forgotten pdb breakpoint :D
  * dont re-create db when app instantiates
  * moved file
  * updated readme, changed view argument
  * dont block when sending emails
  * Merge branch 'feat-user-profile-page' into 'master'
  * fixed verify_token
  * added functionality for updating/resetting password, updating profile
  * return data from verify_token model func not user
  * dont allow subscribe to self in profile page
  * Merge branch 'feature-user-subscriptions' into 'master'
  * added subscriptions link to sidebar, some lift up
  * added subscription checkbox to profiles, added endpoints
  * added subscription functionality, improved API, fixed sorting bookmarks
  * catch exception if db exists on creation
  * lift up
  * moved adding new bookmark from menu to floating button
  * convert request arg 'page' to int, fixes #7
  * return empty string if title wasn't found, fixes #8
  * create database when creating app
  * removed inline js, updated materialize to v0.97.8, fixed voting, fixes #6
  * build image on master only
  * load dev config with manage.py
  * fixed links for fonts/jquery
  * Delete .travis.yml
  * Update .gitlab-ci.yml
  * Update .gitlab-ci.yml
  * Update .gitlab-ci.yml
  * Update .gitlab-ci.yml
  * Update .gitlab-ci.yml
  * Update .gitlab-ci.yml
  * Update .gitlab-ci.yml
  * Update .gitlab-ci.yml
  * Update .gitlab-ci.yml
  * Update .gitlab-ci.yml
  * Update .gitlab-ci.yml
  * Update .gitlab-ci.yml
  * Update .gitlab-ci.yml
  * Update .gitlab-ci.yml
  * Update README.md
  * Update .gitlab-ci.yml
  * Update .gitlab-ci.yml
  * Update .gitlab-ci.yml
  * Update .gitlab-ci.yml
  * Update README.md
  * Update README.md
  * Update README.md
  * Update .gitlab-ci.yml
  * Update .gitlab-ci.yml
  * Update .gitlab-ci.yml
  * Update .gitlab-ci.yml
  * Update .gitlab-ci.yml
  * Update .gitlab-ci.yml
  * Add .gitlab-ci.yml
  * fixed docker image
  * fixed docker repository
  * decoupled sending email
  * removed instance folder,all configs in one file
  * show docker logs after travis failure
  * build travis for dev
  * make docker image work in development
  * added docker
  * added dockerfile
  * import debugtoolbar only in developmnet
  * use production requirements
  * added wsgi file
  * added production requirements
  * added api auth tests
  * updated README
  * added API endpoints
  * refactored voting
  * added relationships to User model, fine-grained the queries a bit, minor changes
  * added Sentry service
  * fixed adding bookmark bug, fixed default category
  * Update README.md
  * Update README.md
  * Update README.md
  * moved some endpoints to bookmarks.py, refactoring
  * fixed bookmark post method, gather all js scripts in bookmark_options.js
  * fixed saved bookmarks using the new script
  * added post method for bookmarks
  * removed unnecessary materialize.js, materialize.css
  * added recaptcha on registration
  * added route for getting 1 bookmark
  * delete bookmark by sending DELETE method request
  * idiomatic python
  * handle saving non existent bookmark
  * updated readme
  * save bookmark with PUT method only
  * make csrf object importable
  * Merge pull request #4 from ev-agelos/materialize
  * fixed test, minor template change
  * updated readme
  * removed bookmarks/categories and bookmarks/categories/name, improved request args for sorting and filtering by category
  * removed action from forms
  * fixed redirect for bookmark deletion
  * treat category with lowercase
  * redirect to login after logout
  * fixed remember me when login
  * fixed log in/out redirects
  * fixed url passing title instead of bookmark id
  * use register.html again, fixed tests
  * replaced bootstrap for materialize plus some small changes
  * Added tests
  * improved sql query, make token.py mockable for pytest
  * remove nullable for Category model
  * Remove app context dependency
  * Initialize CSRF after configuration is loaded
  * Disable CSRF and DebugToolbar when testing
  * Removed .coveragerc, run coverage on bookmarks cause project has better structured now
  * Use UserMixin from Flask-Login, added Flask-Migrate for database migrations
  * fixed import
  * Re-structured project
  * Ignore html coverage folder
  * Added coveragerc, cover all files
  * Fixed folder app for coveralls
  * Simplified voting code
  * Small html/jinja refactoring
  * Fixed category list space
  * Removed serialization passing queries to jinja
  * Changed the backref from bookmarks to user model
  * Added humanization of times when listing bookmarks
  * Changed default thumbnail to python logo
  * Face lift
  * Updated to latest flask: 0.11
  * Fixed 'delete' route
  * Minor fix
  * Fixed flask-debug toolbar to be initialised after config is loaded
  * Updated libraries
  * Updated libraries
  * Updated Flask-Login to latest:0.3.2
  * The save link is the second element after edit link
  * Only last token should be valid, dont allow users activating other user's account
  * Updated readme
  * Added delete endpoint/functionality to each bookmark
  * Fixed bug when updating bookmark's category
  * Changed method names
  * Added boilerplate for search endpoint, not imlemented yet
  * Added category list select box when adding new bookmark
  * Facelift 2
  * Some facelift but still looks ugly
  * Removed AppEnglight for OpBeat service
  * Fixed appenlight env variable
  * Added AppEnlight service
  * Forgot to change the config to use mailgun
  * Parse and return the url title if external request is not allowed
  * Fixed bug when making external requests
  * Removed Flask-Mail for mailgun
  * Fixed voting issue
  * Moved get user/s endpoints to auth package
  * Fixed import
  * Use relative imports
  * Moved Login and Register form to auth package
  * Removed unnecessary __init__ files
  * Removed boomark_views folder
  * Added main app and moved there appropriate code, moved templates/static there too
  * Fixed bug when query doesnt include models as result
  * Dont search users if logged in user requests his categories
  * Renamed folder
  * Moved User model and everything related to auth package
  * Removed not used DebugConfig
  * Added email verification/account activation when user registers.
  * Changed how configs are loaded, added Flaks-Mail
  * Removed redundant requirements
  * Removed redundant requirements
  * Removed python-bcrypt, update library version
  * Added license
  * Adding first commit for documentation
  * Created sphinx files for readthedocs
  * Load instance config if no config passed.
  * Made config kwarg and check if config was passed.
  * Added readthedocs badge
  * oh well fixed required.io
  * Final fix for required.io
  * Minor change
  * Minor change
  * Fixed required.io badge
  * Added required.io badge
  * Updated travis to use pytest-cov for coveralls
  * Used Blueprints.Used Flaks-SQLAlchemy again cause paginator works now, sqlalchemy_wrapper is still required, needs refactoring.
  * Added config, moved code from run.py to __init__ to make tests run/pass and app to run too.
  * Fixed testing configuration
  * Ignore .coverage
  * Ignore .cache
  * Added boilerplate for tests and a simple test case.Changed structure of imports
  * Added coveralls to travis
  * Minor
  * Added coveralls badge
  * Added build badge
  * Fixed py.test command for travis
  * Fixed travis
  * Fixed travis extennsion
  * Added .travis.yaml
  * Saving functionality, needs work still
  * Updated Readme
  * Added basic functionality/endpoints for saving bookmarks.Still needs work
  * added bookmark_views for bookmark endpoints, fixed imports
  * Added route for getting all user's bookmarks
  * Removed get_all_user_bookmarks, instead 'all' as category name is accepted
  * Fixed user categories
  * Refactored user_bookmarks to use serialization and the custom_render
  * Make ordering default to new bookmarks
  * Fixed downloading thumbnail
  * Ignore downloaded images when testing except the default.png
  * Fixed paginator number
  * Fixed ordering
  * Fixed active tab when ordering bookmarks
  * Now index accepts ordering too
  * Made prettier the datetime
  * Added Schemas. Added check if images exist otherwise use the default
  * Moved the check of image in utils
  * Updated README
  * Updated README
  * Download url's image and show it next to the url when listing bookmarks
  * Fixed distances when listing bookmarks
  * Delete FBDefaultIcon_contra.png
  * Added basic functionality to download url's image.For now set a default one for every new bookmark
  * Final fix ignoring instance/
  * Fixed ignoring instance/
  * Added instance/ to gitignore
  * Fixed readme
  * Updated Readme
  * Suggest title button 'suggests' link's page title
  * Updated Readme
  * Updated Readme
  * Updated Readme
  * Updated Readme
  * Updated Readme
  * Added again flask-debug toolbar, if debug==False then toolbar is not used
  * Removed Flask-DebugToolbar from requirements
  * Added development options for application
  * Updated readme
  * Html refactoring
  * Added alerts for flashed messages
  * Added todo.txt to ignored files
  * Added suggest title button when adding a new bookmark to grab websites title but code is not functional yet
  * Refactored site style with bootstrap, refactored the vote script, now users can vote their own bookmarks
  * Html refactor
  * Added order_by to Bookmarks endpoints and also now the links(new,oldest,top,unpopular) work(only for Bookmark endpoints, for now).
  * Minor refactor
  * Added index.py for home endpoint
  * Renamed app folder, moved bookmark endpoints regarding /users/ to users.py
  * Changed the structure to Flask-Classy plugin.
  * Fixed url_for now that Flask-Classy is used, removed a temporarely url
  * Fixed pep257
  * Fixed import and pep8
  * Registed UsersView and BookmarksView classes as Flask-Classy says
  * Fixed pep257
  * Added utils with helped function paginate for View classes to use.
  * Fixed imports for flask extensions, removed session when calling db.
  * Added Flask-Classy to requirements.
  * Added __init__ to views to be able to import after fixing pylint errors, renamed module bookmarks.py to not conflict import with the package bookmarks.
  * Added config option in order to show queries in flask debug toolbar.
  * Moved getting flashed message to base.html so all templates can show them, fixed voting bug for unauthenticated users.
  * Update README.md
  * Updated README
  * updated README
  * Implemented g for user in all templates, refactored html code, now queries include votes where votes where added as a bookmark attribute, general refactoring.
  * Replaced g.user for current_user, changed initialization of flask extensions
  * Fixed forgetten argument in paginate result
  * Moved CRUD bookamarks to its own file, Forgot to git rm migrations and manage.py.
  * Added pagination for endpoints, removed migrations/ and manage.py, refactored code
  * Changed from Flask-Sqlalchemy to SQLAlchemy-Wrapper in order to use pagination in db.session, code is not affected yet. Removed Flask-Migrate from requirements as it needs Flask-Sqlalchemy. Decision has to be made for migrations...
  * Added forgotten votes to bookmarks when requesting home.Changed my_script to change the color of arrow color instead of background, fixed list_bookmarks.html
  * Now home page shows the latest 5 bookmarks
  * Fixed voting system, changed voting script accepting from bookmark_id to bookmark title
  * Changed from ids to username/bookmark title/category name when getting a url.
  * Fixed README.
  * Fixed README.
  * Fixed README.
  * Fixed README.
  * Fixed README.
  * Fixed README.
  * Fixed README.
  * Fixed README.
  * Added endpoints to README.
  * Added datetime field in models, created new database.
  * Added Users link to the navbar.
  * Now all bookmarks show the username that they were added from.
  * Now users cant vote their own bookmarks.
  * Fixed voting.
  * Added votes db table(re-created db), refactored my_script.js and function vote_bookmark, voting is not finished yet.
  * Refactored javascript function and hmtl code
  * Added basic rating functionality to bookmarks, fixed db path.
  * Removed blueprints, removed login_required from some endpoints.
  * Fixed import
  * Updated gitignore
  * Fixed import.
  * Removed redundant relationshop, refactored code.
  * Optimized queries, refactored code.
  * Added import endpoint/functionality
  * Added users/ endpoint
  * Removed pycache folders
  * fixed untracked files
  * Updated gitignore
  * Updated gitignore
  * Updated requirements.
  * Refactored update url endpoint, now each user's url has an edit button next to it, minor changes.
  * Splitted some functions to carry 1 url route, added exception when requesting bookmarks/categories from other user, now templates extend base.html
  * Restractured to be a package, changed urls to be more like restful api
  * Added new clean database.
  * Added forget config.ini
  * Removed migrations to start over a clean one, removed secret key for config.
  * Category model now has its own table, restractured models/relationships.
  * Added editing functionality for user's bookmarks.
  * Added register functionality
  * Added remember me for login.
  * Added secret key.
  * Login now checks password with the hashed one from database.Added registration
  * Fixed database name.
  * Added requirements
  * Added Flask-Bcrypt for hashing user passwords.
  * Added flask-migrate and file manage.py to manage migrations.
  * Added My bookmarks showing logged in User's bookmarks.
  * Added OneToMany relationship for User to Bookmarks.
  * Deleted views/views.py
  * Renamed views.py to bookmarks.py
  * Added views folder, fixed imports.
  * Renamed base.html to list_bookmarks.html, fixed views.
  * Added username to User model, added jinja2 blocks to templates, minor changes/fixes.
  * Merge branch 'master' of https://github.com/ev-agelos/Python-bookmarks
  * First commit
  * Initial commit
