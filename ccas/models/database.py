import sqlite3


def new_query(command):
    operating_database = sqlite3.connect("ccas/ccas_main_database.db")
    cur = operating_database.cursor()
    cur.execute(command)
    table = cur.fetchall()
    return table

def insert_new(command, args=()):
    operating_database = sqlite3.connect("ccas/ccas_main_database.db")
    cur = operating_database.cursor()
    cur.execute(command, args)
    operating_database.commit()
    return True

