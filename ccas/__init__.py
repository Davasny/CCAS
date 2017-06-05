from flask import Flask
import hashlib, time
import sqlite3
import os.path
import ccas.models.database


if not os.path.isfile("ccas/ccas_main_database.db"):
    print("First run")
    ccas.models.database.first_run()

app = Flask('ccas')
app.config['SECRET_KEY'] = str(hashlib.sha256(str(time.time()).encode('utf-8')).hexdigest())

import ccas.models
import ccas.controller
