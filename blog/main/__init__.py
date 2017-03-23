from libs.blueprints import BluePrintProxy


blog_main_bp = None


def sub_main_bp(real_bp, template_folder):
    global blog_main_bp
    blog_main_bp = BluePrintProxy(real_bp, 'main', __name__, template_folder=template_folder)
    from . import views  # enable @rule
    from . import errors
