from libs.blueprints import RecursiveBluePrint


login_bp = None


def sub_login_bp(parent_bp):
    global login_bp
    login_bp = RecursiveBluePrint(parent_bp, 'login', __name__)
    from . import views
