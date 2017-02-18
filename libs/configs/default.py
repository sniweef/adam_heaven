import os


class Config(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # 追踪对象的修改并且发送信号
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(os.path.abspath('.'), 'data.sqlite')
    # SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # SQLALCHEMY_RECORD_QUERIES = True
    # SQLALCHEMY_DATABASE_URI = ''
