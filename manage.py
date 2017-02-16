from flask import Flask
from flask.ext.script import Manager
from flask_wtf.csrf import CsrfProtect


def create_app():
    app = Flask('AdamHeaven')

    CsrfProtect(app)
    return app


def set_up_modules(app, manager):
    from db import set_up_db
    set_up_db(app, manager)


def scan_blueprints(app):
    from blog import get_blog_bp
    blog_bp = get_blog_bp()

    app.register_blueprint(blog_bp, url_prefix='/blog')

if __name__ == '__main__':
    app = create_app()
    manager = Manager(app)

    set_up_modules(app, manager)
    scan_blueprints(app)

    import sys
    for module in sys.modules:
        print(module)

    manager.run()
