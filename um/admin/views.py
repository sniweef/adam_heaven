from flask_security import current_user
from flask_security.utils import encrypt_password
from flask_admin.contrib import sqla
from flask import abort, redirect, url_for, request
from passlib.hash import pbkdf2_sha512
from libs.logger import logger
from flask import current_app


class AccessCheckView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        # if current_user.has_role('superuser'):
        #    return True

        return True

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
        org_pwd = form.password.data
        encrypted_pwd = encrypt_password(org_pwd)

        logger.info('Encrypt password {} to {}'.format(org_pwd, encrypted_pwd))
        form.password.data = encrypted_pwd
        super(AccessCheckView, self).create_model(form)
