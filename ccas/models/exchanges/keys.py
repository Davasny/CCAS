import hashlib, base64
from ccas.models import database
from flask import request
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import json

def get_key(type, exchange):
    response = database.new_query("SELECT `" + type + "` FROM exchanges_api_keys WHERE `exchange`='" + exchange + "';")
    #out = decrypt_key(str(response[0][0])).decode('utf-8')
    return decrypt_key(str(response[0][0]))


def save_keys(exchange, public_key, private_key):
    encrypted_public_key = encrypt_key((public_key)).decode('utf-8')
    encrypted_private_key = encrypt_key((private_key)).decode('utf-8')

    args = (exchange, encrypted_public_key, encrypted_private_key)
    response = database.insert_new("INSERT INTO exchanges_api_keys (`exchange`,`public_key`,`private_key`) VALUES (?, ?, ?) ;", args)
    print(response)
    return True

def encrypt_key(plain_key):
    plain_key = pad(plain_key.encode(), 16)
    iv = Random.new().read(AES.block_size)
    key = hashlib.sha256(request.cookies.get('password').encode()).digest()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    out = base64.b64encode(iv + cipher.encrypt(plain_key))
    return out

def decrypt_key(key):
    return_reposne = {}
    try:
        encrypted = base64.b64decode(key)
        iv = encrypted[:AES.block_size]
        key = hashlib.sha256(request.cookies.get('password').encode()).digest()

        cipher = AES.new(key, AES.MODE_CBC, iv)
        out = unpad(cipher.decrypt(encrypted[AES.block_size:]), 16)
        return_reposne["status"] = True
        return_reposne["data"] = out

    except Exception as e:
        return_reposne["status"] = False
        if e == "Padding is incorrect.":
            return_reposne["msg"] = e

    return return_reposne

