import json
from datetime import date
import logging
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from .controles_models import Control
from constants import Config, HTTPMethods
from flask import jsonify, make_response

logging.basicConfig(level=logging.DEBUG)

engine = create_engine(Config.DB_PATH, echo=True)

Session = sessionmaker()
Session.configure(bind=engine)


def controles_manager(request):
    r_method = request.method
    if r_method == HTTPMethods.GET:
        return get_controles(request)
    elif r_method == HTTPMethods.POST:
        return create_control(request)
    elif r_method == HTTPMethods.PUT:
        return update_control(request)
    elif r_method == HTTPMethods.DELETE:
        return delete_control(request)


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


def query_params_parser(query_params):
    possible_params = ["valor", "unidades", "fecha", "comida"]
    new_query_params = {}
    for param in query_params:
        if param in possible_params:
            new_query_params[param] = query_params[param]
    return new_query_params


def get_controles(request):
    query_params = request.args
    actual_params = query_params_parser(query_params=query_params)
    session = Session()
    if len(query_params) == 0 or len(actual_params) == 0:
        controles = session.query(Control).all()
        controles = controles_parser(controles)
    else:
        controles = session.query(Control).filter_by(**actual_params).all()
        controles = controles_parser(controles)
    session.close()
    return jsonify({"Controles": controles, "Registros": len(controles)})


def create_control(request):
    json_request = request.json
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
    except IntegrityError:
        return make_response({"Error": f"A registry with date: {json_request['fecha']} and meal: {json_request['comida']} already exists"}, 409)


def update_control(request):
    """
        Formato para actualizar un registro
    {
        "fecha": "2020-03-15",
        "comida": "Almuerzo",
        "update": {
            "unidades": 1,
            "valor": 130
        }
    }

    """
    json_request = request.json
    if json_request is None:
        return make_response({"Error": "No JSON request"}, 400)
    try:
        fecha_control = fecha_parser(json_request["fecha"])
        comida_control = json_request["comida"]
        fields_to_update = json_request["update"]
        session = Session()

        control_to_update = session.query(Control).filter_by(fecha=fecha_control, comida=comida_control).first()

        if control_to_update is None:
            session.close()
            return make_response({"Error": "Control not found"}, 404)
        
        unidades_updated = control_to_update.unidades
        valor_updated = control_to_update.valor
        
        if len(fields_to_update) == 0:
            session.close()
            return make_response({"Error": "Fields to update are null"}, 204)
        for field in fields_to_update:
            if field == "unidades":
                unidades_updated = fields_to_update[field]
            elif field == "valor":
                valor_updated = fields_to_update[field]
            else:
                session.close()
                return make_response({"Error": "Fields to update are null"}, 204)
        
        control_to_update.unidades = unidades_updated
        control_to_update.valor = valor_updated
        control_to_update_json = control_to_update.to_json()
        session.commit()
        session.close()
        return make_response({"OK": control_to_update_json}, 200)
    except KeyError:
        return make_response({"Error": "Bad request. Missing key in JSON request"}, 406)


def delete_control(request):
    json_request = request.json
    if json_request is None:
        return make_response({"Error": "No JSON request"}, 400)
    try:
        fecha_control = json_request["fecha"]
        comida_control = json_request["comida"]
        session = Session()
        control_to_delete = session.query(Control).filter_by(fecha=fecha_control, comida=comida_control).first()
        if control_to_delete is None:
            return make_response({"Error": "Control not found"}, 404)
        session.delete(control_to_delete)
        session.commit()
        session.close()
        return make_response({"OK": "Control deleted"}, 200)
    except KeyError:
        return make_response({"Error": "Bad request. Missing key in JSON request"}, 406)
