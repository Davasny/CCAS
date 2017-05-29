from . import poloniex
from ccas.models import database

def get_balances(exchange, public_key, secret_key):
    if exchange == "poloniex":
        return poloniex.get_balances(public_key, secret_key)

def get_exchanges():
    response = database.new_query("SELECT id, exchange FROM exchanges_api_keys;")
    return list(response)
