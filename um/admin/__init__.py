from flask.ext.admin import Admin, AdminIndexView
from flask.ext.admin.contrib.sqla import ModelView
from flask_security import Security, SQLAlchemyUserDatastore
from db import db
from ..models import *
from .views import AccessCheckView


def set_up_admin(app, *args):
    admin = Admin(app, index_view=AdminIndexView(url='/um/admin'))
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Role, db.session))


def set_up_security(app, *args):
    # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)
