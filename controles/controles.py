from datetime import date
import json
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from .controles_models import Control
from constants import Config, HTTPMethods
from flask import jsonify, make_response

engine = create_engine(Config.DB_PATH, echo=True)

Session = sessionmaker()
Session.configure(bind=engine)


def controles_manager(request):
    r_method = request.method
    if r_method == HTTPMethods.GET:
        return get_controles(request)
    elif r_method == HTTPMethods.POST:
        return create_control(request)


def controles_parser(controles):
    controles_list = []
    for control in controles:
        control_json = control.to_json()
        controles_list.append(control_json)
    return controles_list


def fecha_parser(fecha):
    fecha_content = fecha.split('-')
    if len(fecha_content) != 3:
        return make_response({"Error": "Date invalid format. Use AAAA-MM-DD"}, 406)
    year = int(fecha_content[0])
    month = int(fecha_content[1])
    day = int(fecha_content[2])
    new_date = date(year, month, day)
    return new_date


def get_controles(request):
    session = Session()
    controles = session.query(Control).all()
    session.close()
    controles = controles_parser(controles)
    return jsonify({"Controles": controles, "Registros": len(controles)})


def create_control(request):
    json_request = request.json
    print("******************************************************************")
    print(f"{request}")
    print(f"{request.json}")
    print(f"{request.headers}")
    print(f"{request.data}")
    print("******************************************************************")
    if json_request is None:
        return make_response({"Error": "No JSON request"}, 400)
    try:
        fecha_control = fecha_parser(json_request["fecha"])
        comida_control = json_request["comida"]
        unidades_control = json_request["unidades"]
        valor_control = json_request["valor"]
        new_control = Control(fecha=fecha_control, comida=comida_control,
                              unidades=unidades_control, valor=valor_control)
        control_json = new_control.to_json()
        session = Session()
        session.add(new_control)
        session.commit()
        session.close()
        return make_response({"Created": control_json}, 201)
    except KeyError:
        return make_response({"Error": "Missing key in JSON request"}, 400)
    return {}


def update_control(request):
    return {}


def delete_control(request):
    return {}
