import collections
from ccas import app
from ccas.models import currency, exchanges
from ccas.models.exchanges import keys
from flask import render_template, request, make_response, redirect
from ccas.models.currency import wallets, groups
from ccas.models import database, dashboard, coinmarketcap, password
from decimal import *
import configparser
import hashlib


config = configparser.ConfigParser()
config.read("ccas/config.ini")


@app.route('/')
@app.route('/dashboard')
def dashboard_view():
    return render_template('dashboard.html')



@app.route('/dashboard_content')
def dashboard_content():
    supported_currency = config["Currency"]["supportedCurrency"].split(",")
    balances = []
    errors = []

    tmp_group = []
    for new_currency in supported_currency:
        all_wallets = wallets.get_addresses_with_names(new_currency) # wallets without group

        if all_wallets:
            new_response = currency.get_details(new_currency, all_wallets, "balance")
            if True in new_response.values():
                balances.extend(new_response["data"])
            else:
                errors.append("Something went wrong with " + new_currency + " - " + str(new_response['msg']))

        all_groups = groups.get_groups_for(new_currency)

        group_balances = []
        for group in all_groups:
            all_wallets = wallets.get_address_by_group(group[0])

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
    if password.check_if_pass():
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


    btc_price = exchanges.get_btc_price()

    # [CURRENCY, PLACE, AMOUNT, PRICE, TYPE, NAME]
    total_btc = sum_all_balances(balances)
    columns_to_show = dashboard.get_column_to_show()

    return render_template('dashboard_content.html', balances=balances, total_btc=total_btc, errors=errors, btc_price=btc_price,
                           columns_to_show=columns_to_show)


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
    if request.referrer is not None and '/exchanges' in request.referrer:
        keys.remove_key(id)
    response = make_response(redirect("/exchanges"))
    return response



@app.route('/exchanges/new', methods=['GET', 'POST'])
def exchanges_new():
    if request.method == 'POST' :
        if password.check_if_pass():
            exchange = request.form['exchange']
            public_key = request.form['public_key']
            private_ley = request.form['private_key']

            keys.save_keys(exchange, public_key, private_ley)

    response = make_response(redirect("/exchanges"))

    return response



######### WALLETS #########
@app.route('/wallets')
def wallets_view():
    supported_currency = config["Currency"]["supportedCurrency"].split(",")

    all_wallets = []
    for wallet in currency.get_all_wallets():
        tmp_wallet = []
        tmp_wallet.append(wallet[0])
        tmp_wallet.append(wallet[1])
        tmp_wallet.append(wallet[2])
        tmp_wallet.append(wallet[3])

        all_wallets.append(tmp_wallet)

    # [id, currency, name, address]
    return render_template('wallets.html', possible_currency=supported_currency, wallets=all_wallets )



@app.route('/wallets/remove/<id>')
def wallets_remove(id):
    if request.referrer is not None and '/wallets' in request.referrer:
        wallets.remove_wallet(id)
    response = make_response(redirect("/wallets"))
    return response



@app.route('/wallets/new', methods=['GET', 'POST'])
def wallets_new():
    if request.method == 'POST':
        currency = request.form['currency']
        address = request.form['address'].split()
        name = request.form['name']

        for new_address in address:
            wallets.save_wallet(currency, new_address, name)

    response = make_response(redirect("/wallets"))
    return response
######### WALLETS #########



######### GROUPS #########
@app.route('/groups')
def groups_view():
    supported_currency = config["Currency"]["supportedCurrency"].split(",")

    all_groups = []
    for group in groups.get_all_groups():
        tmp_group = []
        tmp_group.append(group[0])
        tmp_group.append(group[2])
        tmp_group.append(group[1])
        tmp_group.append(wallets.get_address_by_group(group[0]))
        all_groups.append(tmp_group)

    # [id, currency, name, wallets]
    return render_template('groups.html', supported_currency=supported_currency, groups=all_groups )



@app.route('/groups/new', methods=['GET', 'POST'])
def groups_new():
    if request.method == 'POST':
        currency = request.form['currency']
        name = request.form['name']
        new_group_id = groups.create_new_group(name, currency)

        response = make_response(redirect("/groups/edit/" + str(new_group_id)))
    else:
        response = make_response(redirect("/groups"))
    return response



@app.route('/groups/edit/<group_id>', methods=['GET', 'POST'])
def groups_edit(group_id):
    all_wallets = []
    if request.referrer is not None and '/groups' in request.referrer:
        messages = []
        if 'save' in request.form:
            group_name = request.form['name']
            args = (group_id,)
            database.new_argument_query("DELETE FROM wallet_group WHERE group_id=?", args)
            for key, val in request.form.items():
                if key != 'name' and key != 'save':
                    args = (key, group_id)
                    database.new_argument_query("INSERT INTO wallet_group (`wallet_id`,`group_id`) VALUES (?, ?) ;", args)
            database.new_argument_query("UPDATE groups SET `name`=? WHERE `id`=?;", (group_name, group_id))
            messages.append("Saved!")

        elif 'cancel' in request.form:
            return make_response(redirect("/groups"))

        group_details = groups.get_group_details(group_id)
        group_name = group_details[0]
        group_currency = group_details[1]
        group_wallets = wallets.get_address_by_group(group_id)

        for wallet in currency.get_all_wallets(group_currency):
            tmp_wallet = []

            tmp_wallet.append(wallet[0])
            tmp_wallet.append(wallet[2])
            tmp_wallet.append(wallet[3])

            if wallet[3] in group_wallets:
                tmp_wallet.append(True)
            else:
                tmp_wallet.append(False)

            all_wallets.append(tmp_wallet)
        # [id, name, address, state (in group or not)]
        return render_template('groups_edit.html', group_id=group_id, all_wallets=all_wallets, group_name=group_name, messages=messages)
    else:
        return make_response(redirect("/groups"))



@app.route('/groups/remove/<id>')
def groups_remove(id):
    if request.referrer is not None and '/groups' in request.referrer:
        groups.remove_group(id)
    response = make_response(redirect("/groups"))
    return response
######### GROUPS #########



######### PASSWORD #########
@app.route('/use_password', methods=['GET', 'POST'])
def use_password():
    if request.method == 'POST':
        response = make_response(redirect(request.referrer))
        hash_password = ''
        if 'clear' not in request.form and request.form['password'] != '':
            new_password = request.form['password']
            hash_password = password.generate_hash(new_password)
            response.set_cookie('password', hash_password)
        else:
            response.set_cookie('password', hash_password, expires=0)
        return response
    else:
        return dashboard_view()
######### PASSWORD #########



######### SETTINGS #########
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    messages = []
    if request.method == 'POST' and 'cols_save' in request.form:
        if 'cols_setting' in request.form:
            for key, val in request.form.items():
                if key != 'save':
                    bool = True if val=="on" else False
                    dashboard.update_column(key, bool)

        elif 'prices_setting' in request.form:
            a = 1
    elif request.method == 'POST' and 'prices_save' in request.form:
        for key, val in request.form.items():
            if 'save' not in key:
                val = 'coinmarketcap' if 'CMC' in val else val
                currency.update_coin_prices_settings(key.lower(), val)


    all_currency = list(config["Currency"]["supportedCurrency"].split(","))
    all_exchanges = list(config["Exchanges"]["supportedExchanges"].split(","))
    all_exchanges.sort()

    for new_currency in coinmarketcap.get_all_settings():
        all_exchanges.append('CMC_' + new_currency[1])

    for new_currency in currency.get_coin_prices_settings():
        if new_currency[1].upper() not in all_currency:
            all_currency.append(new_currency[1].upper())


    known_currecy={} # {'BTC':'bitfinex', 'LTC':'btc-e'}
    for new_currency in currency.get_coin_prices_settings():
        if new_currency[1].upper() in all_currency:
            if new_currency[2] == 'coinmarketcap':
                known_currecy[new_currency[1].upper()] = 'CMC_' + new_currency[1]
            else:
                known_currecy[new_currency[1].upper()] = new_currency[2]

    return render_template('settings_dashboard.html', columns_data=dashboard.get_columns_details(), all_currency=all_currency, all_exchanges=all_exchanges, known_currecy=known_currecy, messages=messages)



######### SETTINGS CMC #########
@app.route('/settings_coinmarketcap')
def settings_coinmarketcap():
    all_settings = coinmarketcap.get_all_settings()
    return render_template('settings_coinmarketcap.html', all_settings=all_settings)


@app.route('/settings_coinmarketcap/new', methods=['GET', 'POST'])
def settings_coinmarketcap_new():
    if request.method == 'POST':
        currency = request.form['currency']
        cmc_link = request.form['cmc_link']
        cmc_id = (cmc_link if cmc_link[-1:]!="/" else cmc_link[:-1]).split("/")[-1]

        coinmarketcap.create_new_currency(currency, cmc_id)

    return make_response(redirect("/settings_coinmarketcap"))


@app.route('/settings_coinmarketcap/remove/<id>')
def settings_coinmarketcap_remove(id):
    if request.referrer is not None and '/settings_coinmarketcap' in request.referrer:
        coinmarketcap.remove_currency(id)
    response = make_response(redirect("/settings_coinmarketcap"))
    return response
######### SETTINGS CMC #########



######### SETTINGS PASSWORD #########
@app.route('/settings_password', methods=['GET', 'POST'])
def settings_password():
    messages = []
    hash_password = ''

    if request.referrer is not None and '/settings_password' in request.referrer:
        old_pass = request.form['old_pass']
        new_pass = request.form['new_pass']
        new_pass2 = request.form['new_pass2']

        if password.generate_hash(old_pass) == password.get_current_pass():
            if new_pass == new_pass2:
                keys.update_all_keys(old_pass, new_pass)
                hash_password = password.generate_hash(new_pass)
                messages.append('Password changed!')

    response = make_response(render_template('settings_password.html', messages=messages))
    if hash_password != '':
        response.set_cookie('password', hash_password)


    return response

######### SETTINGS PASSWORD #########



@app.route('/settings/database')
def settings_database():
    return render_template('settings_database.html')

######### SETTINGS #########


@app.context_processor
def utility_processor():
    return dict(get_pass_hash=password.get_pass_hash_short, check_if_pass=password.check_if_pass)



def sum_all_balances(balances):
    sum = 0
    for balance in balances:
        if balance[3] != -1:
            sum += Decimal(balance[2]*balance[3])
    return sum

