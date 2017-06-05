from . import database
import hashlib
from flask import request


def generate_hash(new_password):
    return hashlib.sha256(new_password.encode('utf-8')).hexdigest()


def check_if_pass():
    print(check_if_first_run())

    if 'password' in request.cookies and request.cookies['password'] != 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855':
        return True
    else:
        return False


def get_pass_hash_short():
    password = request.cookies.get('password')
    return password[:5] + " [...] " + password[len(password) - 5:]


def get_current_pass():
    return request.cookies.get('password')


def check_if_first_run():
    response = database.new_query("SELECT `value` FROM `settings` WHERE `name`='pass_made' ;")[0][0]
    return True if 'False' in response else False


def made_first_run():
    return database.new_argument_query("UPDATE `settings` SET `value`='True' WHERE `name`='pass_made' ;", ())
