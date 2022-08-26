import logging
from flask import request, render_template, url_for, redirect
from constants import HTTPMethods
from controles.managers import ControlesManager
from models import db_access, app_f

# App start
app = app_f
logging.basicConfig(level=logging.DEBUG)

# Database config
db = db_access

# Managers
controles_manager = ControlesManager(db.session)


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
