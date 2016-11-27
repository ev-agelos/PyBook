from flask_script import Manager

from flask_migrate import Migrate, MigrateCommand

from bookmarks import db, create_app

app = create_app('config.DevConfig')

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


if __name__ == '__main__':
    manager.run()
