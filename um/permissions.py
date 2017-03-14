from flask_security import current_user
from functools import wraps
from flask import abort


class AcquiredPermission:
    ROOT = 'Root'
    ADMIN = 'Admin'
    POST_ARTICLE = 'PostArticle'
    POST_COMMENTS = 'PostComments'
    # READ = 'Reader'


def has_permission(permission_need):
    if permission_need is None:
        return True

    for role in current_user.roles:
        for permission in role.permissions:
            if permission.name == AcquiredPermission.ROOT:
                return True

            if permission.name == permission_need:
                return True

    return False


def permission_acquired(permission):

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if has_permission(permission):
                return f(*args, **kwargs)
            else:
                abort(403)

        return wrapper

    return decorator