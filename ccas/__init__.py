from flask import Flask
import hashlib, time
import sqlite3
import os.path


if not os.path.isfile("ccas/ccas_main_database.db"):
    print("First run")
    if os.path.isfile("ccas/db_startup_config.txt"):
        print("Creating database")

        f = open("ccas/db_startup_config.txt", "r")
        lines = f.readlines()

        operating_database = sqlite3.connect("ccas/ccas_main_database.db")
        for line in lines:
            print(line)
            cur = operating_database.cursor()
            cur.execute(line)

        operating_database.commit()

app = Flask('ccas')
app.config['SECRET_KEY'] = str(hashlib.sha256(str(time.time()).encode('utf-8')).hexdigest())

import ccas.models
import ccas.controller
