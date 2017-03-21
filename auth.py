from functools import wraps

from flask import session

import util

import users


def check_auth(email, password):
    """
    This function is called to check if a user is in the DB and if the password matches
    """
    user = users.usersDB.get(email)
    if user:
        if password == user.password:
            return user
    return None


def check_credentials():
    user = session.get('user', None)
    user_auth = session.get('user_auth', None)
    if user and user_auth:
        print(user, user_auth)
        return check_auth(user, user_auth)
    return False



def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        return f(*args, **kwargs) if check_credentials() else "Not authorized!"
    return decorated
