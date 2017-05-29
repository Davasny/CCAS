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
    errors = []

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
        new_response = exchanges.get_balances(new_exchange)
        if False in new_response.values():
            errors.append("Something went wrong with keys for "+ new_exchange +". Please check password again")
        else:
            balances.extend(new_response["data"])


    # [CURRENCY, PLACE, AMOUNT, PRICE]
    return render_template('dashboard.html', balances=balances, errors=errors)

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

@app.route('/use_password', methods=['GET', 'POST'])
def use_password():
    if request.method == 'POST':
        password = request.form['password'].encode('utf-8')
        hash_password = hashlib.sha256(password).hexdigest()

        reponse = make_response(redirect("/dashboard"))
        reponse.set_cookie('password', hash_password)
        return reponse
    else:
        return dashboard()
@app.context_processor
def utility_processor():
    def get_pass_hash():
        password = request.cookies.get('password')
        return password[:5] + " [...] " + password[len(password) - 5:]

    def check_if_pass():
        if 'password' in request.cookies:
            return True
        else:
            return False

    return dict(get_pass_hash=get_pass_hash, check_if_pass=check_if_pass)
