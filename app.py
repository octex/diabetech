import logging
from flask import Flask, request, render_template, url_for, redirect
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
    return redirect("/diabetech/", code=302)


@app.route('/diabetech/', methods=[HTTPMethods.GET])
def diabetech():
    return render_template("index.html")


@app.route('/diabetech/controles/', methods=[HTTPMethods.GET])
def controles():
    return controles_manager.get_controles(request)


@app.route('/diabetech/controles/agregar/', methods=[HTTPMethods.GET, HTTPMethods.POST])
def agregar_controles():
    return controles_manager.add_control(request)
