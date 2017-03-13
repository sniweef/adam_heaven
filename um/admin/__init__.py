from flask.ext.admin import Admin, AdminIndexView
from flask.ext.admin.contrib.sqla import ModelView
from flask_security import Security, SQLAlchemyUserDatastore
from flask_admin import helpers as admin_helpers
from flask import url_for
from db import db
from ..models import *
from .views import AccessCheckView


def set_up_admin(app, *args):
    admin = Admin(app, base_template='my_master.html', template_mode='bootstrap3')

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    admin.add_view(AccessCheckView(User, db.session))
    admin.add_view(AccessCheckView(Role, db.session))
    admin.add_view(AccessCheckView(Permission, db.session))

    @security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=admin_helpers,
            get_url=url_for
        )
