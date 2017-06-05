from ccas.models import database


def get_column_to_show():
    response = database.new_query(
        "SELECT `name`,`value` FROM settings WHERE name LIKE 'dash_show_%' ;")
    columns_data = {}
    for column in response:
        if column[1] == 'True':
            columns_data[column[0]] = True
        else:
            columns_data[column[0]] = False

    return columns_data


def get_columns_details():
    response = database.new_query(
        "SELECT `name`,`value`,`description` FROM settings WHERE name LIKE 'dash_show_%' ;")
    columns_data = []
    for column in response:
        tmp_data = []
        tmp_data.append(column[0])

        if column[1] == 'True':
            tmp_data.append(True)
        else:
            tmp_data.append(False)

        tmp_data.append(column[2])
        columns_data.append(tmp_data)
    return columns_data


def update_column(name, new_value):
    args = (str(new_value), name)
    return database.new_argument_query("UPDATE settings SET `value`=? WHERE `name`=? ;", args)


def get_refresh_interval():
    return database.new_query("SELECT `value` FROM `settings` WHERE `name`='dash_interval'")[0][0]


def save_new_time(time):
    return database.new_argument_query("UPDATE settings SET `value`=? WHERE `name`='dash_interval' ;", (time, ))
