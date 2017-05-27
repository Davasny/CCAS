from ccas.models import database


def get_all_groups(currency):
    raw_data = database.new_query("SELECT id, name FROM groups WHERE currency='" + currency + "' ;")

    all_addresses = [([0] * 2) for i in range(len(raw_data))]

    #response = []
    i = 0
    for row in raw_data:
        all_addresses[i][0] = row[0]
        all_addresses[i][1] = row[1]
        #response.append(row[0])
        i += 1
    return all_addresses
