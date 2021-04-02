import logging
from flask import Flask, request, Request, jsonify
from analisis import analisis
from controles import controles
from insumos import insumos
from turnos import turnos
from constants import HTTPMethods

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/', methods=[HTTPMethods.GET])
def home():
    return jsonify({"test": 1})

@app.route('/controles/')
def controles():
    return {}

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
