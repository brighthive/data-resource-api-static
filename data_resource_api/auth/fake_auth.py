""" A fake authentication decorator.

"""

from functools import wraps
from flask import request
from flask_restful import abort
from data_resource_api.app.app import db
from data_resource_api.db import Token


def abort_unauthorized():
    abort(401, message='Unauthorized Resource Access.')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            token = str(request.headers['Authorization'])
            token = token.split(' ')
            if str(token[0]).upper() == 'BEARER' and len(token[1]) > 0:
                found_token = Token.query.filter_by(token=token[1]).first()
                if found_token is None:
                    abort_unauthorized()
            else:
                abort_unauthorized()
        except Exception:
            abort_unauthorized()
        return f(*args, **kwargs)
    return decorated_function
