from flask_security import current_user
from flask_security.utils import encrypt_password
from flask_admin.contrib import sqla
from flask import abort, redirect, url_for, request
from libs.logger import logger
from flask import current_app
from ..permissions import AcquiredPermission, has_permission


class AccessCheckView(sqla.ModelView):
    column_exclude_list = ['password', 'content']

    def __init__(self, *args, **kwargs):
        self.permission = kwargs.pop('permission', AcquiredPermission.ADMIN)
        super(AccessCheckView, self).__init__(*args, **kwargs)

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        return has_permission(self.permission)

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))

    def create_model(self, form):
        try:
            org_pwd = form.password.data
            encrypted_pwd = encrypt_password(org_pwd)

            logger.info('Encrypt password {} to {}'.format(org_pwd, encrypted_pwd))
            form.password.data = encrypted_pwd
        except AttributeError:
            pass

        super(AccessCheckView, self).create_model(form)
