import json
from datetime import datetime

from flask import render_template, jsonify
from constants import HTTPMethods, HTTPCodes, Config

from sqlalchemy import DATETIME, Column, Integer, create_engine, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class ControlesManager:
    def __init__(self, db_manager):
        self.db = db_manager
        self.db_session = self.db.get_session()

    def add_control(self, request):
        r_method = request.method
        if r_method == HTTPMethods.GET:
            return render_template("add_control.html")
        elif r_method == HTTPMethods.POST:
            return self.create_db_model(request.json)

    def create_db_model(self, request):
        new_control = Control()
        try:
            new_control.valor = request["valor"]
            new_control.fecha = datetime.strptime(request["fecha"], "%Y-%m-%dT%M:%S")
            new_control.insulina = request["insulina"]
            new_control.observaciones = request["observaciones"]
            self.db_session.add(new_control)
            self.db_session.commit()
        except KeyError as e:
            return DiabetechResponse(HTTPCodes.BAD_REQUEST, e).get_response()
        new_control_api = ControlApi(new_control)
        return DiabetechResponse(HTTPCodes.CREATED, new_control_api.to_json()).get_response()

    def remove_control(self, request):
        pass

    def get_controles(self, request):
        # controles = Control.query.paginate(page=1, per_page=10)
        controles = self.db_session.query(Control).all()
        controles_api = []
        for control in controles:
            control_api = ControlApi(control)
            controles_api.append(control_api)
        return render_template("controles.html", controles=controles_api)


class DbManager:
    def __init__(self, database):
        self.engine = create_engine(database, echo=True)
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()

    def get_session(self):
        return self.session


class Control(Base):
    __tablename__ = 'controles'
    control_id = Column(Integer, primary_key=True)
    valor = Column(Integer)
    fecha = Column(DATETIME)
    insulina = Column(Integer)
    observaciones = Column(String)


class ControlApi:
    def __init__(self, control_model):
        self.valor = control_model.valor
        self.fecha = self.get_date_from_model(control_model.fecha)
        self.hora = self.get_hour_from_model(control_model.fecha)
        self.insulina = control_model.insulina
        self.observaciones = control_model.observaciones

    def get_date_from_model(self, date):
        return date.strftime("%d-%m-%Y")

    def get_hour_from_model(self, date):
        return date.strftime("%H:%M:%S")
    
    def to_json(self):
        model = {
            "valor": self.valor,
            "fecha": self.fecha,
            "hora": self.hora,
            "insulina": self.insulina,
            "observaciones": self.observaciones
        }
        return model


class DiabetechResponse:
    def __init__(self, http_code, message):
        self.http_code = http_code
        self.message = message
    
    def to_json(self, dumped=False):
        model = {
            "code": self.http_code,
            "message": self.message
        }
        if dumped:
            model = json.dumps(model)
        return model

    def get_response(self, for_flask=True):
        response = self.to_json()
        if for_flask:
            response = jsonify(response)
        return response


def create_tables(engine):
    Base.metadata.create_all(engine)
