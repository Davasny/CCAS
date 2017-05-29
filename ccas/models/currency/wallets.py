from ccas.models import database

def get_raw_addresses(currency):
    raw_data = database.new_query("select wallets.address from wallets where (parent_group is NULL or parent_group = '') AND currency='"+ currency +"' ;")
    response = []
    for row in raw_data:
        response.append(row[0])
    return response

def get_addresses_with_names(currency):
    raw_data = database.new_query("select wallets.address, wallets.name from wallets where (parent_group is NULL or parent_group = '') AND currency='"+ currency +"' ;")
    response = []
    for row in raw_data:
        tmp_list = []
        tmp_list.append(row[0])
        tmp_list.append(row[1])

        response.append(tmp_list)
    return response

def get_addresses(currency):
    raw_data = database.new_query("select wallets.address from wallets left join groups on groups.id=wallets.parent_group WHERE wallets.currency='"+ currency +"' order by wallets.currency;")
    response = []
    for row in raw_data:
        response.append(row[0])

    return response

def get_all_wallets(currency):
    response = database.new_query("select wallets.currency, wallets.address, wallets.name, groups.name from wallets\
     left join groups on groups.id=wallets.parent_group WHERE wallets.currency='"+ currency +"'\
      order by wallets.currency;")
    return response

def get_address_by_group(group_id):
    raw_data = database.new_query("SELECT address FROM wallets WHERE parent_group='"+ str(group_id) +"' ;")
    response = []
    for row in raw_data:
        response.append(row[0])
    return response
