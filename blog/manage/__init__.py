from libs.blueprints import BluePrintProxy


manage_blog_bp = None


def sub_manage_bp(real_bp, template_folder):
    global manage_blog_bp
    manage_blog_bp = BluePrintProxy(real_bp, 'manage', __name__, url_prefix='/manage',
                                    template_folder=template_folder)
    from . import views  # enable @rule
