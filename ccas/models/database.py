import sqlite3
import os.path


def new_query(command):
    operating_database = sqlite3.connect("ccas/ccas_main_database.db")
    cur = operating_database.cursor()
    cur.execute(command)
    table = cur.fetchall()
    return table

def new_argument_query(command, args=()):
    operating_database = sqlite3.connect("ccas/ccas_main_database.db")
    cur = operating_database.cursor()
    cur.execute(command, args)
    operating_database.commit()
    return cur.lastrowid


def first_run():
    if os.path.isfile("ccas/db_startup_config.txt"):
        print("Creating database")

        f = open("ccas/db_startup_config.txt", "r")
        lines = f.readlines()

        if os.path.isfile("ccas/ccas_main_database.db"):
            os.remove("ccas/ccas_main_database.db")

        operating_database = sqlite3.connect("ccas/ccas_main_database.db")
        for line in lines:
            cur = operating_database.cursor()
            cur.execute(line)

        operating_database.commit()
        return True
    return False
