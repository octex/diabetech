from flask import render_template
from constants import HTTPMethods

from sqlalchemy import DATETIME, Column, Integer, create_engine, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class ControlesManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def handle_request(self, request):
        r_method = request.method
        if r_method == HTTPMethods.GET:
            return self.get_controles(request)
        elif r_method == HTTPMethods.POST:
            return self.add_control(request)
        elif r_method == HTTPMethods.DELETE:
            return self.remove_control(request)

    def add_control(self, request):
        return render_template("add_control.html")

    def remove_control(self, request):
        pass

    def get_controles(self, request):
        return render_template("add_control.html")

    def generate_page():
        pass


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

    def get_date_from_model(date):
        return date.strftime("%d-%m-%Y")

    def get_hour_from_model(date):
        return date.strftime("%H:%m:%S")


def create_tables(engine):
    Base.metadata.create_all(engine)
