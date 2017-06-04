import time
import urllib
import urllib.request
import json
from decimal import *
from . import database
from flask import g
import configparser
import os

config = configparser.ConfigParser()
config.read("ccas/config.ini")
cmc_file_name = config['General']['cmcTempFile']


def get_price(currency):
    download_data()
    parsed = json.load(open(cmc_file_name, 'r'))

    currency_id = database.new_query("SELECT `id_on_cmc` FROM `cmc_currency_settings` WHERE `name`='" + currency.lower() + "'")
    if currency_id:
        currency_id = currency_id[0][0]
    else:
        return -1

    if parsed['prices'][currency_id]:
        return Decimal(parsed['prices'][currency_id])
    else:
        return -1


def download_data():
    get_new = True
    current_time = int(time.time())

    if os.path.isfile(cmc_file_name):
        data = json.load(open(cmc_file_name, 'r'))
        old_time = data['date']
        if old_time:
            if (current_time - old_time) < (10):
                get_new = False

    if get_new:
        f = open(cmc_file_name, 'w+')

        return_reposne = {}
        return_reposne['date'] = current_time

        raw_json = urllib.request.urlopen('https://api.coinmarketcap.com/v1/ticker/')
        parsed = json.loads(raw_json.read().decode('utf-8'))

        tmp_response = {}
        for currency in parsed:
            if currency['price_btc'] is not None:
                tmp_response[currency['id']] = currency['price_btc']

        return_reposne['prices'] = tmp_response
        f.write(json.dumps(return_reposne, ensure_ascii=False))
        f.close()

    return True


def get_all_settings():
    response = database.new_query(
        "SELECT `id`, `name`, `id_on_cmc` FROM cmc_currency_settings;")
    return response


def create_new_currency(currency, cmc_id):
    return database.new_argument_query("INSERT INTO `cmc_currency_settings` (`name`, `id_on_cmc`) VALUES (?, ?)", (currency, cmc_id))


def remove_currency(id):
    return database.new_argument_query("DELETE FROM `cmc_currency_settings` WHERE `id`=? ;", (id,))
