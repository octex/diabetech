import json
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
