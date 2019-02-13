""" A fake authentication decorator.

"""

from functools import wraps
from flask import request
from flask_restful import abort


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            token = str(request.headers['Authorization'])
            token = token.split(' ')
            if str(token[0]).upper() == 'BEARER' and len(token[1]) > 0:
                pass
            else:
                abort(401)
        except Exception:
            abort(401)
        return f(*args, **kwargs)
    return decorated_function
