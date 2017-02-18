from flask.ext.admin import Admin, AdminIndexView
from flask.ext.admin.contrib.sqla import ModelView
from flask_security import Security, SQLAlchemyUserDatastore
from db import db
from flask_admin import helpers as admin_helpers
from ..models import *
from .views import AccessCheckView


def set_up_admin(app, *args):
    admin = Admin(app, index_view=AdminIndexView(url='/um/admin'))

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    admin.add_view(AccessCheckView(User, db.session))
    admin.add_view(AccessCheckView(Role, db.session))

    @security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=admin_helpers,
            get_url=url_for
        )