from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand


class DbManager(object):
    db = SQLAlchemy()
    migrate = None
    set_up = False

    @staticmethod
    def set_up_db(app, manager):
        if not DbManager.set_up:
            DbManager.db.init_app(app)

            from um.models import User, Role

            DbManager.migrate = Migrate(app, DbManager.db)
            manager.add_command('db', MigrateCommand)

            DbManager.set_up = True


db = DbManager.db
