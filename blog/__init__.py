from flask import Blueprint
from libs.logger import logger


def get_blog_bp():
    blog_bp = Blueprint('blog', __name__)
    from blog.main import add_sub_main_bp
    add_sub_main_bp(blog_bp)

    from libs.scanner import SourceScanner
    for _, name in SourceScanner('blog/', r'add_sub_(\w+)_bp').apply_scanned_function(blog_bp):
        logger.info('Append sub blueprint <{}> for blog'.format(name))

    return blog_bp
