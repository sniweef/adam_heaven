from libs.blueprints import RecursiveBluePrint


blog_main_bp = None


def sub_main_bp(parent_bp, template_folder):
    global blog_main_bp
    blog_main_bp = RecursiveBluePrint(parent_bp, 'main', __name__, template_folder=template_folder)
    from . import views  # enable @rule
