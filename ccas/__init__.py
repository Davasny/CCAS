from flask import Flask
app = Flask('ccas')
#app.config['SECRET_KEY'] = 'random'

import ccas.models
import ccas.controller
