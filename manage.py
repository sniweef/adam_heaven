from flask import Flask
from flask.ext.script import Manager
from flask_wtf.csrf import CsrfProtect
from libs.logger import logger


def create_app():
    app = Flask('AdamHeaven')

    CsrfProtect(app)
    return app


def set_up_modules(app, manager):
    from db import set_up_db
    set_up_db(app, manager)

    # from libs import replace_logger_with
    # replace_logger_with(app.logger)


def scan_blueprints(app):
    from libs.scanner import SourceScanner

    for bp, bp_name in SourceScanner('.', r'get_(\w+)_bp').apply_scanned_function():
        bp_url_prefix = '/' + bp_name
        app.register_blueprint(bp, url_prefix=bp_url_prefix)
        logger.info('Register blueprint: {} for url_prefix: {}'.format(bp, bp_url_prefix))

if __name__ == '__main__':
    app = create_app()
    manager = Manager(app)

    set_up_modules(app, manager)
    scan_blueprints(app)

    import sys
    # for module in sys.modules:
        # print(module)

    manager.run()
