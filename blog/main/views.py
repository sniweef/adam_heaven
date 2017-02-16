from blog.main import blog_main_bp


@blog_main_bp.route('/test')
def test():
    return 'test'
