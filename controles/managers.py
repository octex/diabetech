from datetime import datetime

from flask import render_template
from constants import HTTPMethods, HTTPCodes, Config

from controles.models import Control, ControlApi
from models import DiabetechResponse

class ControlesManager:
    def __init__(self, session):
        self.db = session

    def add_control(self, request):
        r_method = request.method
        if r_method == HTTPMethods.GET:
            return render_template("add_control.html", result=None)
        elif r_method == HTTPMethods.POST:
            return self.create_db_model(request.json)

    def create_db_model(self, request):
        new_control = Control()
        try:
            new_control.valor = request["valor"]
            new_control.fecha = datetime.strptime(request["fecha"], "%Y-%m-%dT%H:%M")
            new_control.insulina = request["insulina"]
            new_control.observaciones = request["observaciones"]
            self.db.add(new_control)
            self.db.commit()
        except KeyError as e:
            response = DiabetechResponse(HTTPCodes.NOT_ACCEPTABLE, e)
            return render_template("add_control.html", result=response.to_json())
        except ValueError as e:
            response = DiabetechResponse(HTTPCodes.BAD_REQUEST, e)
            return render_template("add_control.html", result=response.to_json())
        new_control_api = ControlApi(new_control)
        response = DiabetechResponse(HTTPCodes.CREATED, new_control_api.to_json())
        return render_template("add_control.html", result=response.to_json())

    def remove_control(self, request):
        pass

    def get_controles(self, request):
        page = request.args.get('page', 1, type=int)
        controles = Control.query.paginate(page=page, per_page=Config.MAX_PAGINATION_SET)
        controles_api = []
        for control in controles.items:
            control_api = ControlApi(control)
            controles_api.append(control_api)
        return render_template("controles.html", controles=controles_api, controles_paged=controles)
