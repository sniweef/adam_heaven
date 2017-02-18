from flask import Blueprint
from libs.logger import logger
from libs.utils import register_sub_bp


def get_blog_bp():
    blog_bp = Blueprint('blog', __name__)
    register_sub_bp('blog/', blog_bp)

    return blog_bp
