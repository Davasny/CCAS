from flask import Flask
import hashlib, time


app = Flask('ccas')
app.config['SECRET_KEY'] = str(hashlib.sha256(str(time.time()).encode('utf-8')).hexdigest())

import ccas.models
import ccas.controller
