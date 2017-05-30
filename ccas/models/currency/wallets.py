from ccas.models import database

def get_raw_addresses(currency):
    raw_data = database.new_query("select wallets.address from wallets where (parent_group is NULL or parent_group = '') AND currency='"+ currency +"' ;")
    response = []
    for row in raw_data:
        response.append(row[0])
    return response

def get_addresses_with_names(currency):
    raw_data = database.new_query("select wallets.address, wallets.name, wallets.id from wallets where currency='"+ currency +"' ;") # (parent_group is NULL or parent_group = '') AND
    response = []
    for row in raw_data:
        tmp_list = []
        tmp_list.append(row[0])
        tmp_list.append(row[1])
        tmp_list.append(row[2])

        response.append(tmp_list)
    return response


def get_addresses(currency):
    raw_data = database.new_query("select wallets.address from wallets left join groups on groups.id=wallets.parent_group WHERE wallets.currency='"+ currency +"' order by wallets.currency;")
    response = []
    for row in raw_data:
        response.append(row[0])

    return response


# def get_all_wallets(currency):
#     response = database.new_query("select wallets.currency, wallets.address, wallets.name, groups.name, wallets.id from wallets\
#      left join groups on groups.id=wallets.parent_group WHERE wallets.currency='"+ currency +"'\
#       order by wallets.currency;")
#
#     response = database.new_query("SELECT id, currency, address, name FROM wallets WHERE currency='"+ currency +"'")
#     return response


def get_address_by_group(group_id):
    raw_data = database.new_query("select wallets.address from wallets inner join wallet_group on wallets.id=wallet_group.wallet_id and wallet_group.group_id="+ str(group_id) +";")
    response = []
    for row in raw_data:
        response.append(row[0])
    return response


def save_wallet(currency, address, name):
    args = (currency, address, name)
    database.new_argument_query(
        "INSERT INTO wallets (`currency`,`address`,`name`) VALUES (?, ?, ?) ;", args)
    return


def remove_wallet(id):
    args = (id,)
    response = database.new_argument_query("DELETE FROM wallets WHERE `id`=? ;", args)
    return response
