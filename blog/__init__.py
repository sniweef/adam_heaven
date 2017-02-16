from flask import Blueprint


def get_blog_bp():
    blog_bp = Blueprint('blog', __name__)
    from blog.main import add_sub_main_bp
    add_sub_main_bp(blog_bp)

    return blog_bp
