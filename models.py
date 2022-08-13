from sqlalchemy import DATETIME, Column, Integer, create_engine, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class ControlesManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def add_control(self, control):
        pass

    def remove_control(self, control_id):
        pass

    def get_controles(self):
        pass

    def get_controles_by_filters(filters):
        pass

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

Base.metadata.create_all()