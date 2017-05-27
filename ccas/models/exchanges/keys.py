from ccas.models import database

def get_key(type, exchange):
    response = database.new_query("SELECT `" + type + "` FROM exchanges_api_keys WHERE `exchange`='" + exchange + "';")
    return str(response[0][0])