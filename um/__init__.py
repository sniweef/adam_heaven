import os
from flask import Blueprint
from libs.utils import register_sub_bp
from um.admin import set_up_admin  # keep this
from .models import *


#def get_um_bp():
#    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
#    auth_bp = Blueprint('UserManager', __name__, template_folder=template_dir)

#    register_sub_bp('um/', auth_bp)

#    return auth_bp
def deploy_product_data():
    Permission.insert_permissions()
    Role.insert_roles()
    User.insert_root()
