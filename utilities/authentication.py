from functools import wraps
from typing import Optional

import jwt
from flask import request, make_response

from app import LOG
from models.administration import User
from repository.setup_sqlalchemy import sql_engine
from repository.user import UserRepository


def create_token(username: str) -> str:
    return jwt.encode({'username': username}, 'secret', algorithm='HS256')

def process_token(token: str) -> Optional[User]:
    try:
        # LOG.info('process_token a')
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        # LOG.info('process_token b')
        # LOG.info(payload)
        # LOG.info('process')
        user = UserRepository(sql_engine).get_by_username(payload['username'])
        return user
    except Exception as e:
        return None

def auth(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            token = request.headers.get('Authorization')
            user = process_token(token)
            if not user:
                return make_response('', 401)
            return f(user, *args, **kwargs)
        except Exception as e:
            return make_response('', 401)
    return decorator

