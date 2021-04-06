import json
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from constants import Config


Base = declarative_base()
engine = create_engine(Config.DB_PATH, echo=True)


class Analisis(Base):

    __tablename__ = 'analisis'

    tipo = Column(String())
    medico = Column(String())
    fecha = Column(Date())


    __mapper_args__ = {"eager_defaults": True}
    __table_args__ = (
        PrimaryKeyConstraint('medico', 'tipo'),
    )

    def to_json(self):
        data = {"fecha": str(self.fecha), "medico": self.medico, "tipo": self.tipo}
        return data

    def __repr__(self):
        return "<Analisis(fecha='%s', medico='%s', tipo='%s')>" % (
            self.fecha, self.medico, self.tipo)


Base.metadata.create_all(engine)