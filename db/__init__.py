from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand


class DbManager(object):
    db = SQLAlchemy()
    migrate = None
    set_up = False

    @staticmethod
    def set_up_db(app, manager):
        if not DbManager.set_up:
            DbManager.db.init_app(app)

            from um.models import User, Role, Permission
            from blog.models import ArticleType, Source, Article, Comment, Follow, Menu, ArticleTypeSetting,\
                BlogInfo, Plugin

            DbManager.migrate = Migrate(app, DbManager.db)
            manager.add_command('db', MigrateCommand)

            DbManager.set_up = True


db = DbManager.db
