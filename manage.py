import os
from flask import Flask
from flask.ext.script import Manager
from flask_wtf.csrf import CsrfProtect
from libs.logger import logger
from libs.scanner import SourceScanner
from libs.configs import load_config


def create_app():
    app = Flask('AdamHeaven')

    os.environ['MODE'] = 'DEVELOPMENT'
    app.config.from_object(load_config())
    CsrfProtect(app)
    return app


def set_up_modules(app, manager):
    from db import DbManager
    DbManager.set_up_db(app, manager)

    for _, name in SourceScanner('.', r'set_up_(\w+)').apply_scanned_function(app, manager):
        logger.info('Set up module: {}'.format(name))


def scan_blueprints(app):
    for bp, bp_name in SourceScanner('.', r'get_(\w+)_bp').apply_scanned_function():
        bp_url_prefix = '/' + bp_name
        app.register_blueprint(bp, url_prefix=bp_url_prefix)
        logger.info('Register blueprint: {} for url_prefix: {}'.format(bp, bp_url_prefix))

if __name__ == '__main__':
    app = create_app()
    manager = Manager(app)

    set_up_modules(app, manager)
    scan_blueprints(app)

    manager.run()
