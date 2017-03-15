from libs.blueprints import RecursiveBluePrint


manage_blog_bp = None


def sub_manage_bp(parent_bp, template_folder):
    global manage_blog_bp
    manage_blog_bp = RecursiveBluePrint(parent_bp, 'manage', __name__, url_prefix='/manage',
                                        template_folder=template_folder)
    from . import views  # enable @rule