from os import getenv
from flask import render_template, Flask
app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import routes
