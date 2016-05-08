"""The secret sauce to solve circural dependencies issues."""


from bookmarks import create_app, db


if __name__ == '__main__':
    app = create_app()
    app.run()
