from ccas.models import database


def get_groups_for(currency):
    raw_data = database.new_query("SELECT id, name FROM groups WHERE currency='" + currency + "' ;")

    all_groups = [([0] * 2) for i in range(len(raw_data))]

    i = 0
    for row in raw_data:
        all_groups[i][0] = row[0]
        all_groups[i][1] = row[1]
        i += 1
    return all_groups


def get_group_details(id):
    raw_data = database.new_query("SELECT name, currency FROM groups WHERE id='" + id + "' ;")
    return list(raw_data[0])


def get_all_groups():
    raw_data = database.new_query("SELECT id, name, currency FROM groups;")

    all_groups = [([0] * 3) for i in range(len(raw_data))]

    i = 0
    for row in raw_data:
        all_groups[i][0] = row[0]
        all_groups[i][1] = row[1]
        all_groups[i][2] = row[2]
        i += 1
    return all_groups


def create_new_group(name, currency):
    args = (name, currency)
    return database.new_argument_query("INSERT INTO groups (`name`,`currency`) VALUES (?, ?) ;", args)


def remove_group(id):
    args = (id,)
    database.new_argument_query("DELETE FROM groups WHERE `id`=? ;", args)
    database.new_argument_query("DELETE FROM wallet_group WHERE `group_id`=? ;", args)
    return True





