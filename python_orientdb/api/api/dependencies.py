import pyorient

from api.settings import orient


def get_orient():
    return orient


def handle_token_expiration(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except pyorient.exceptions.PyOrientSecurityAccessException:
            orient.connect(get_orient())
            return func(*args, **kwargs)

    return wrapper
