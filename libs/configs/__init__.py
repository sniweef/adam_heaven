# encoding=utf-8
import os
from libs.logger import logger


def load_config():
    """Load config"""
    mode = os.environ.get('MODE')
    logger.info('Current mode: ' + mode)

    try:
        if mode == 'PRODUCTION':
            from .production import ProductionConfig
            return ProductionConfig
        elif mode == 'TESTING':
            from .testing import TestingConfig
            return TestingConfig
        else:
            from .development import DevelopmentConfig
            return DevelopmentConfig
    except ImportError as e:
        from .default import Config
        return Config
