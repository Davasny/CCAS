import collections
from ccas import app
from ccas.models import currency, exchanges
from flask import render_template, request, make_response, redirect
from ccas.models.currency import wallets, groups
from decimal import *
import configparser
import hashlib


@app.route('/')
@app.route('/dashboard')
def dashboard():
    config = configparser.ConfigParser()
    config.read("ccas/config.ini")
    supported_currency = config["Currency"]["supportedCurrency"].split(",")
    supported_exchanges = config["Exchanges"]["supportedExchanges"].split(",")
    balances = []


    tmp_group = []
    for new_currency in supported_currency:
        all_wallets = wallets.get_raw_addresses(new_currency) # wallets without group
        balances.extend(currency.get_details(new_currency, all_wallets, "balance"))

        # get group
        all_groups = groups.get_all_groups(new_currency)

        # send wallets to get balances
        group_balances = []
        for group in all_groups:
            all_wallets = wallets.get_address_by_group(group[0])  # wallets without group

            if all_wallets:
                group_balances.append(new_currency)
                group_balances.append(group[1])
                group_balances.append(0)

                group_details = currency.get_details(new_currency, all_wallets, "balance")
                if group_details:
                    for wallet in group_details:
                        group_balances[2] += Decimal(wallet[2])
                    group_balances.append(group_details[0][3])
                    group_balances.append("GROUP")
                tmp_group.append(group_balances)
    balances.extend(tmp_group)

    # loooop through all exchanges
    for new_exchange in supported_exchanges:
        balances.extend(exchanges.get_balances(new_exchange))


    # [CURRENCY, PLACE, AMOUNT, PRICE]
    return render_template('dashboard.html', balances=balances)

@app.route('/exchanges')
def exchanges_view():
    list_of_addresses = []
    list_of_addresses.append("1DfQZXnJuWnKLMgJhtso3Px7sLLGKhjk9j")
    list_of_addresses.append("1MDUoxL1bGvMxhuoDYx6i11ePytECAk9QK")
    balances = currency.get_details("BTC", list_of_addresses, "balance")
    return render_template('exchanges.html', balances=balances)

@app.route('/settings')
def settings():
    list_of_addresses = []
    list_of_addresses.append("1DfQZXnJuWnKLMgJhtso3Px7sLLGKhjk9j")
    list_of_addresses.append("1MDUoxL1bGvMxhuoDYx6i11ePytECAk9QK")
    balances = currency.get_details("BTC", list_of_addresses, "balance")
    return render_template('settings.html', balances=balances)


