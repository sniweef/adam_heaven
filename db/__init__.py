from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand


class DbManager(object):
    db = SQLAlchemy()
    migrate = None


def set_up_db(app, manager):
    DbManager.migrate = Migrate(app, DbManager.db)
    manager.add_command('db', MigrateCommand)
