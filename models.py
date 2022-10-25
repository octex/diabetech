import os
import csv
import json
from datetime import datetime
from flask import jsonify, Flask
from flask_sqlalchemy import SQLAlchemy


app_f = Flask(__name__)
app_f.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///diabetech.db"
db_access = SQLAlchemy(app_f)


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

class CsvReport:
    def __init__(self, headers, data):
        self.default_dir = './diabetech_' + datetime.today().strftime("%d%m%Y") + ".csv"
        self.file = open(self.default_dir, 'w')
        self.writer = csv.writer(self.file)
        self.headers = headers
        self.data = data
    
    def write_headers(self):
        self.writer.writerow(self.headers)
    
    def write_data(self):
        self.writer.writerows(self.data)

    def get_file(self):
        self.file.close()
        return self.default_dir

    def __del__(self):
        if os.path.exists(self.default_dir):
            os.remove(self.default_dir)
