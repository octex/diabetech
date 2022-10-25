import logging
from datetime import datetime

from flask import render_template, send_file
from constants import HTTPMethods, HTTPCodes, Config

from controles.models import Control, ControlApi
from models import CsvReport, DiabetechResponse

class ControlesManager:
    def __init__(self, session):
        self.db = session

    def add_control(self, request):
        r_method = request.method
        if r_method == HTTPMethods.GET:
            return render_template("add_control.html", result=None)
        elif r_method == HTTPMethods.POST:
            return self.add_control_registry(request.json)

    def add_control_registry(self, request):
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
        control_id = request.args.get('control_id', None, type=int)
        if not control_id:
            response = DiabetechResponse(HTTPCodes.NOT_ACCEPTABLE, "Missing param 'coelsa_id'")
            return response.to_json()
        control = self.db.query(Control).filter_by(control_id=control_id).first()
        if not control:
            response = DiabetechResponse(HTTPCodes.NOT_FOUND, f"Control with id: {control_id} not found")
            return response.to_json()
        self.db.delete(control)
        self.db.commit()
        response = DiabetechResponse(HTTPCodes.OK, "Control deleted!")
        return response.to_json()

    def get_controles(self, request):
        result = None
        if request.method == HTTPMethods.DELETE:
            result = self.remove_control(request)
        page = request.args.get('page', 1, type=int)
        return self.generate_paged_controls(page, result)

    def generate_paged_controls(self, page, result_t):
        controles = Control.query.paginate(page=page, per_page=Config.MAX_PAGINATION_SET)
        controles_api = []
        for control in controles.items:
            control_api = ControlApi(control)
            controles_api.append(control_api)
        return render_template("controles.html", controles=controles_api, controles_paged=controles, result=result_t)

    def download_report(self, request):
        controles_raw = self.db.query(Control).all()
        report_data = []
        report_headers = [
            "Valor", "Insulina",
            "Fecha", "Hora",
            "Observaciones"
        ]
        for control in controles_raw:
            report_data.append(ControlApi(control).to_list())
        report = CsvReport(headers=report_headers, data=report_data)
        report.write_headers()
        report.write_data()
        return send_file(report.get_file())
