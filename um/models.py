import hashlib
from flask.ext.login import UserMixin
from db import db
from flask_security import UserMixin, RoleMixin
from werkzeug.security import generate_password_hash, check_password_hash


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


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    avatar_hash = db.Column(db.String(32))
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.email

