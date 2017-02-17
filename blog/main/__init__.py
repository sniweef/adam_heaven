from libs.blueprints import RecursiveBluePrint


blog_main_bp = None


def add_sub_main_bp(parent_bp):
    global blog_main_bp
    blog_main_bp = RecursiveBluePrint(parent_bp, 'blog_main', __name__, url_prefix='/main')
    from . import views  # enable @rule
