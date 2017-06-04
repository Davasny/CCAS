from . import database
import hashlib
from flask import request


def generate_hash(new_password):
    return hashlib.sha256(new_password.encode('utf-8')).hexdigest()


def check_if_pass():
    if 'password' in request.cookies and request.cookies['password'] != 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855':
        return True
    else:
        return False


def get_pass_hash_short():
    password = request.cookies.get('password')
    return password[:5] + " [...] " + password[len(password) - 5:]


def get_current_pass():
    return request.cookies.get('password')
