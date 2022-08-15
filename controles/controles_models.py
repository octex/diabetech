import json
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from constants import Config


# Base = declarative_base()
# engine = create_engine(Config.DB_PATH, echo=True)

class Control:
    __tablename__ = 'controles'

    fecha = Column(Date())
    comida = Column(String())
    valor = Column(Integer())
    unidades = Column(Integer())

    __mapper_args__ = {"eager_defaults": True}
    __table_args__ = (
        PrimaryKeyConstraint('fecha', 'comida'),
    )


    def to_json(self):
        data = {"fecha": str(self.fecha), "comida": self.comida, "unidades": self.unidades, "valor": self.valor}
        return data
    

    def __repr__(self):
        return "<Control(fecha='%s', comida='%s', unidades='%s', valor='%s')>" % (
            self.fecha, self.comida, self.unidades, self.valor)

# Base.metadata.create_all(engine)