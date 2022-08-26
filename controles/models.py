from models import db_access as db


class Control(db.Model):
    __tablename__ = 'controles'
    control_id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DATETIME, nullable=False)
    insulina = db.Column(db.Integer, nullable=False)
    observaciones = db.Column(db.String, nullable=True)


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

db.create_all()