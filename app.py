import logging
from flask import Flask, request
from controles.controles import controles_manager
from insumos import insumos
from analisis.analisis import analisis_manager
from turnos import turnos
from constants import HTTPMethods
from models import DbManager

app = Flask(__name__)
db_manager = DbManager("sqlite://diabetech.db")
logging.basicConfig(level=logging.DEBUG)


@app.route('/', methods=[HTTPMethods.GET])
def home():
    return {}


@app.route('/controles/', methods=[HTTPMethods.GET, HTTPMethods.POST, HTTPMethods.PUT, HTTPMethods.DELETE])
def controles():
    return controles_manager(request)


@app.route('/insumos/')
def insumos():
    return {}


@app.route('/analisis/', methods=[HTTPMethods.GET, HTTPMethods.POST, HTTPMethods.PUT, HTTPMethods.DELETE])
def analisis():
    return analisis_manager(request)


@app.route('/turnos/')
def turnos():
    return {}


@app.route('/informes/')
def informes():
    return {}
