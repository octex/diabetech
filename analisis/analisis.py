import json
import logging
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from .analisis_models import Analisis
from constants import Config, HTTPMethods
from utils import registry_parser, query_params_parser, fecha_parser
from flask import jsonify, make_response


logging.basicConfig(level=logging.DEBUG)

engine = create_engine(Config.DB_PATH, echo=True)

Session = sessionmaker()
Session.configure(bind=engine)


def analisis_manager(request):
    r_method = request.method
    if r_method == HTTPMethods.GET:
        return get_analisis(request)
    elif r_method == HTTPMethods.POST:
        return create_analisis(request)
    elif r_method == HTTPMethods.PUT:
        return update_analisis(request)
    elif r_method == HTTPMethods.DELETE:
        return delete_analisis(request)


def get_analisis(request):
    query_params = request.args
    possible_filter_params = ["medico", "fecha", "tipo"]
    filter_params = query_params_parser(query_params=query_params, possible_params=possible_filter_params)
    session = Session()
    if len(query_params) == 0 or len(filter_params) == 0:
        #TODO: Paginado
        analisis = session.query(Analisis).all()
        analisis = registry_parser(analisis)
    else:
        analisis = session.query(Analisis).filter_by(**filter_params).all()
        analisis = registry_parser(analisis)
    session.close()
    return jsonify({"Analisis": analisis, "Registros": len(analisis)})


def create_analisis(request):
    json_request = request.json
    if json_request is None:
        return make_response({"Error": "No JSON request"}, 400)
    try:
        fecha_analisis = fecha_parser(json_request["fecha"])
        tipo_analisis = json_request["tipo"]
        medico_analisis = json_request["medico"]
        new_analisis = Analisis(fecha=fecha_control, tipo=tipo_analisis, medico=medico_analisis)
        analisis_json = new_analisis.to_json()
        session = Session()
        session.add(new_analisis)
        session.commit()
        session.close()
        return make_response({"Created": analisis_json}, 201)
    except KeyError:
        return make_response({"Error": "Missing key in JSON request"}, 400)
    except IntegrityError:
        return make_response({"Error": f"A registry with date: {json_request['fecha']} and doctor: {json_request['medico']} already exists"}, 409)


def update_analisis(request):
    json_request = request.json
    if json_request is None:
        return make_response({"Error": "No JSON request"}, 400)
    try:
        tipo_analisis = json_request["tipo"]
        medico_analisis = json_request["medico"]
        fields_to_update = json_request["update"]
        session = Session()

        analisis_to_update = session.query(Analisis).filter_by(tipo=tipo_analisis, medico=medico_analisis).first()

        if analisis_to_update is None:
            session.close()
            return make_response({"Error": "Analisis not found"}, 404)
        
        fecha_updated = analisis_to_update.fecha
        
        if len(fields_to_update) == 0:
            session.close()
            return make_response({"Error": "Fields to update are null"}, 204)
        else:
            try:
                fecha_updated = fields_to_update["fecha"]
            except KeyError:
                session.close()
                return make_response({"Error": "Fields to update are null"}, 204)
        
        analisis_to_update.fecha = fecha_updated
        analisis_to_update_json = analisis_to_update.to_json()
        session.commit()
        session.close()
        return make_response({"OK": analisis_to_update_json}, 200)
    except KeyError:
        return make_response({"Error": "Bad request. Missing key in JSON request"}, 406)


def delete_analisis(request):
    json_request = request.json
    if json_request is None:
        return make_response({"Error": "No JSON request"}, 400)
    try:
        medico_analisis = json_request["medico"]
        tipo_control = json_request["tipo"]
        session = Session()
        analisis_to_delete = session.query(Analisis).filter_by(medico=medico_analisis, tipo=tipo_control).first()
        if analisis_to_delete is None:
            return make_response({"Error": "Analisis not found"}, 404)
        session.delete(analisis_to_delete)
        session.commit()
        session.close()
        return make_response({"OK": "Analisis deleted"}, 200)
    except KeyError:
        return make_response({"Error": "Bad request. Missing key in JSON request"}, 406)
