"""The secret sauce to solve circural dependencies issues."""


from main import create_app, db


if __name__ == '__main__':
    app = create_app()
    app.run()
