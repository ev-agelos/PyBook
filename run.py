"""The secret sauce to solve circural dependencies issues."""


from bookmarks_app import app, db


if __name__ == '__main__':
    app.run()
