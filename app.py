import logging
from flask import Flask, request
from controles.controles import controles_manager
from insumos import insumos
from analisis import analisis
from turnos import turnos
from constants import HTTPMethods

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


@app.route('/', methods=[HTTPMethods.GET])
def home():
    return {}


@app.route('/controles/', methods=[HTTPMethods.GET, HTTPMethods.POST, HTTPMethods.PUT])
def controles():
    return controles_manager(request)


@app.route('/insumos/')
def insumos():
    return {}


@app.route('/analisis/')
def analisis():
    return {}


@app.route('/turnos/')
def turnos():
    return {}


@app.route('/informes/')
def informes():
    return {}
