import logging
from flask import Flask, request, render_template, url_for
from constants import HTTPMethods
from models import DbManager, ControlesManager, create_tables

# App start
app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Database config
db_manager = DbManager("sqlite:///diabetech.db")
create_tables(engine=db_manager.engine)

# Managers
controles_manager = ControlesManager(db_manager)


@app.route('/', methods=[HTTPMethods.GET])
def home():
    return render_template("index.html")


@app.route('/controles/', methods=[HTTPMethods.GET, HTTPMethods.POST, HTTPMethods.PUT, HTTPMethods.DELETE])
def controles():
    return controles_manager.handle_request(request)
