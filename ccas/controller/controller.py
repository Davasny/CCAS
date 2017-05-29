import collections
from ccas import app
from ccas.models import currency, exchanges
from ccas.models.exchanges import keys
from flask import render_template, request, make_response, redirect
from ccas.models.currency import wallets, groups
from decimal import *
import configparser
import hashlib


config = configparser.ConfigParser()
config.read("ccas/config.ini")


@app.route('/')
@app.route('/dashboard')
def dashboard():
    supported_currency = config["Currency"]["supportedCurrency"].split(",")
    balances = []
    errors = []

    tmp_group = []
    for new_currency in supported_currency:
        all_wallets = wallets.get_raw_addresses(new_currency) # wallets without group
        balances.extend(currency.get_details(new_currency, all_wallets, "balance"))

        all_groups = groups.get_all_groups(new_currency)

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
    for new_exchange in exchanges.get_exchanges():
        public_key = keys.get_key("public_key", new_exchange[0])
        secret_key = keys.get_key("private_key", new_exchange[0])

        if True in public_key.values() and True in secret_key.values():
            public_key = public_key["data"]
            secret_key = secret_key["data"]
            new_response = exchanges.get_balances(new_exchange[1], public_key, secret_key)

            if True in new_response.values():
                balances.extend(new_response["data"])
            else:
                errors.append("Something went wrong with keys for " + new_exchange[
                    1] + "[" + str(new_exchange[0]) + "] - " + str(new_response['msg']))
        else:
            errors.append("Something went wrong with keys for " + new_exchange[
                1] + "[" + str(new_exchange[0]) + "]. Please check password")


    # [CURRENCY, PLACE, AMOUNT, PRICE]
    return render_template('dashboard.html', balances=balances, errors=errors)


@app.route('/exchanges')
def exchanges_view():
    supported_exchanges = config["Exchanges"]["supportedExchanges"].split(",")

    all_exchanges = []
    for new_exchange in exchanges.get_exchanges():
        tmp_exchange = []
        tmp_exchange.append(new_exchange[0])
        tmp_exchange.append(new_exchange[1])
        public_key = keys.get_key("public_key", new_exchange[0])
        secret_key = keys.get_key("private_key", new_exchange[0])

        if True in public_key.values() and True in secret_key.values():
            public_key_decoded = public_key["data"].decode('utf-8')
            secret_key_decoded = secret_key["data"].decode('utf-8')

            tmp_exchange.append(public_key_decoded[:5] + " [...] " + public_key_decoded[len(public_key_decoded) - 5:])
            tmp_exchange.append(secret_key_decoded[:5] + " [...] " + secret_key_decoded[len(secret_key_decoded) - 5:])

        all_exchanges.append(tmp_exchange)

    # [id, exchange, public_key, private_key]
    return render_template('exchanges.html', possible_exchanges=supported_exchanges, exchanges=all_exchanges )



@app.route('/exchanges/remove/<id>')
def exchanges_remove(id):
    reponse = make_response(redirect("/exchanges"))
    return reponse


@app.route('/exchanges/new', methods=['GET', 'POST'])
def exchanges_new():
    if request.method == 'POST':
        exchange = request.form['exchange']
        public_key = request.form['public_key']
        private_ley = request.form['private_key']

        keys.save_keys(exchange, public_key, private_ley)

    reponse = make_response(redirect("/exchanges"))
    return reponse


@app.route('/use_password', methods=['GET', 'POST'])
def use_password():
    if request.method == 'POST':
        password = request.form['password'].encode('utf-8')
        hash_password = hashlib.sha256(password).hexdigest()

        reponse = make_response(redirect(request.referrer))
        reponse.set_cookie('password', hash_password)
        return reponse
    else:
        return dashboard()


@app.route('/settings')
def settings():
    return render_template('settings.html')


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
