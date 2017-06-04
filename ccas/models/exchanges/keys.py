import hashlib, base64
from ccas.models import database
from flask import request
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import json


def get_key(type, exchange_id):
    response = database.new_query("SELECT `" + type + "` FROM exchanges_api_keys WHERE `id`='" + str(exchange_id) + "';")
    password = request.cookies.get('password')
    return decrypt_key(str(response[0][0]), password)


def save_keys(exchange, public_key, private_key):
    password = request.cookies.get('password')
    encrypted_public_key = encrypt_key((public_key), password).decode('utf-8')
    encrypted_private_key = encrypt_key((private_key), password).decode('utf-8')

    args = (exchange, encrypted_public_key, encrypted_private_key)
    database.new_argument_query("INSERT INTO exchanges_api_keys (`exchange`,`public_key`,`private_key`) VALUES (?, ?, ?) ;", args)

    return True

def remove_key(id):
    args = (id,)
    response = database.new_argument_query("DELETE FROM exchanges_api_keys WHERE `id`=? ;", args)
    return response

def encrypt_key(plain_key, password):
    plain_key = pad(plain_key.encode(), 16)
    iv = Random.new().read(AES.block_size)
    key = hashlib.sha256(password.encode()).digest()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    out = base64.b64encode(iv + cipher.encrypt(plain_key))
    return out

def decrypt_key(key, password):
    return_reposne = {}

    try:
        encrypted = base64.b64decode(key)
        iv = encrypted[:AES.block_size]
        password = hashlib.sha256(password.encode('utf-8')).digest()

        cipher = AES.new(password, AES.MODE_CBC, iv)
        out = unpad(cipher.decrypt(encrypted[AES.block_size:]), 16)
        return_reposne["status"] = True
        return_reposne["data"] = out

    except Exception as e:
        return_reposne["status"] = False
        #if e == "Padding is incorrect.":
        return_reposne["msg"] = e

    return return_reposne


def get_all_keys():
    return database.new_query("SELECT `id`, `public_key`, `private_key` FROM `exchanges_api_keys` ;")


def update_all_keys(old_pass, new_pass):
    old_pass = hashlib.sha256(old_pass.encode('utf-8')).hexdigest()
    new_pass = hashlib.sha256(new_pass.encode('utf-8')).hexdigest()

    for key_pair in get_all_keys():
        pair_id = key_pair[0]

        public_key = (decrypt_key(key_pair[1], old_pass)['data']).decode()
        private_key = (decrypt_key(key_pair[2], old_pass)['data']).decode()

        encrypted_public_key = encrypt_key((public_key), new_pass).decode('utf-8')
        encrypted_private_key = encrypt_key((private_key), new_pass).decode('utf-8')

        args = (encrypted_public_key, encrypted_private_key, pair_id)
        database.new_argument_query("UPDATE exchanges_api_keys SET `public_key`=?, `private_key`=? WHERE `id`=? ;", args)
    return True
