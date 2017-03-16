import hashlib
from flask.ext.login import UserMixin
from db import db
from flask_security import UserMixin, RoleMixin
from flask_security.utils import encrypt_password, verify_password


# Define models
roles_permissions = db.Table(
    'roles_permissions',
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')),
    db.Column('permission_id', db.Integer(), db.ForeignKey('permission.id'))
)


class Permission(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

    @staticmethod
    def insert_permissions():
        data = {
            'Root': 'control everything',
            'ModifyUser': 'add/edit/delete a user',
            'ModifyArticle': 'edit/delete article',
            'ModifyComments': 'edit/delete comments',
            'ModifyOwnComments': "delete/edit user's own comments. the author of article can also edit/delete "
                                 "comments of the article",
            'ModifyOwnArticle': "delete/edit user's own article",
            'PostArticle': 'post a new article',
            'PostComments': 'post a new comment'
        }
        for name, description in data.items():
            if Permission.query.filter_by(name=name).first() is None:
                permission = Permission(name=name, description=description)
                db.session.add(permission)

        db.session.commit()


# Define models
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    permissions = db.relationship('Permission', secondary=roles_permissions,
                                  backref=db.backref('roles', lazy='dynamic'))

    def __str__(self):
        return self.name

    @staticmethod
    def insert_roles():
        data = {
            # Name: [PermissionName, Description]
            'Root': [('Root',), 'Can control everything'],
            'Admin': [('ModifyUser',), 'Role that can only add a user'],
            'ChefEditor': [('ModifyArticle', 'ModifyComments'), 'Editor that can edit all articles'],
            'Poster': [('ModifyOwnComments', 'ModifyOwnArticle', 'PostArticle', 'PostComments'),
                       'Role that can post a article or edit/delete comments'],
            'Maintainer': [('ModifyComments',), 'Role that can edit/delete comments'],
            'Reader': [('ModifyOwnComments', 'PostComments'), 'A base role that can read articles or edit/post '
                                                              'his comment'],
            'Anonymous': [('PostComments',), 'Role that have not login']
        }
        for name, info in data.items():
            if Role.query.filter_by(name=name).first() is None:
                permission_names = info[0]
                permissions = Permission.query.filter(Permission.name in permission_names)
                role = Role(name=name, description=info[1], permissions=permissions)
                db.session.add(role)

        db.session.commit()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nick_name = db.Column(db.String(255), unique=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    avatar_hash = db.Column(db.String(32))
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(
                    self.email.encode('utf-8')).hexdigest()

    def __str__(self):
        return self.email

    def gravatar(self, size=40, default='identicon', rating='g'):
        # if request.is_secure:
        #     url = 'https://secure.gravatar.com/avatar'
        # else:
        #     url = 'http://www.gravatar.com/avatar'
        url = 'http://gravatar.duoshuo.com/avatar'
        hash = self.avatar_hash or hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    @staticmethod
    def insert_root():
        user = User(first_name='Adam', last_name='Huang', email='hzhigeng@qq.com', password='asdfqwer', active=True)
        if User.query.filter_by(email=user.email).first() is None:
            db.session.add(user)
            db.session.commit()

    def verify_password(self, password):
        return verify_password(password, self.password)

    def verify_and_update_password(self, old_password, new_password):
        if verify_password(old_password, self.password):
            self.password = encrypt_password(new_password)
            db.session.add(self)
            db.session.commit()
            return True

        return False
