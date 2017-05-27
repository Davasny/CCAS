import sqlite3
import time
import os
import hmac
import hashlib
import urllib
import urllib.request
import json

from . import btc, eth

def get_details(curerncy, list_of_addresses, type):
    if curerncy == "BTC" and type == "balance":
        return btc.get_balance(list_of_addresses)

    elif curerncy == "ETH" and type == "balance":
        return eth.get_balance(list_of_addresses)

