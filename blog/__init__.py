from flask import Blueprint
from libs.logger import logger
from libs.utils import register_sub_bp
import os.path as op
from .models import *
from flask.ext.moment import Moment
from flask.ext.bootstrap import Bootstrap


moment = Moment()
bootstrap = Bootstrap()


def get_blog_bp():
    template_folder = op.join(op.dirname(__file__), 'templates')
    static_folder = op.join(op.dirname(__file__), 'static')
    blog_bp = Blueprint('blog', __name__, template_folder=template_folder, static_folder=static_folder)
    register_sub_bp('blog/', blog_bp, template_folder)

    return blog_bp


def set_up_blog(app, manager):
    # Global variables to jiajia2 environment:
    app.jinja_env.globals['ArticleType'] = ArticleType
    app.jinja_env.globals['article_types'] = article_types
    app.jinja_env.globals['Menu'] = Menu
    app.jinja_env.globals['BlogInfo'] = BlogInfo
    app.jinja_env.globals['Plugin'] = Plugin
    app.jinja_env.globals['Source'] = Source
    app.jinja_env.globals['Article'] = Article
    app.jinja_env.globals['Comment'] = Comment
    app.jinja_env.globals['BlogView'] = BlogView

    global moment
    moment.init_app(app)
    bootstrap.init_app(app)


def deploy_product_data():
    logger.info('Deploy blog info')
    # step_1:insert basic blog info
    BlogInfo.insert_blog_info()
    # step_2:insert system default setting
    ArticleTypeSetting.insert_system_setting()
    # step_3:insert default article sources
    Source.insert_sources()
    # step_4:insert default article_type
    ArticleType.insert_system_article_type()
    # step_5:insert system plugin
    Plugin.insert_system_plugin()
    # step_6:insert blog view
    BlogView.insert_view()


def deploy_test_data():
    # step_1:insert navs
    Menu.insert_menus()
    # step_2:insert article_types
    ArticleType.insert_article_types()
    # step_3:generate random articles
    Article.generate_fake(10)
    # step_4:generate random comments
    Comment.generate_fake(100)
    # step_5:generate random replies
    Comment.generate_fake_replies(100)
    # step_4:generate random comments
    # Comment.generate_fake(100)
