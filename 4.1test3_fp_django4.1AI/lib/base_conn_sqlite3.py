from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer, Float, UniqueConstraint
import os

# PATH = os.path.abspath(os.path.dirname(__file__))+'\\..\\db\\test.db'


class ConnectSqlite3:
    """
        在其他模块中的使用
        from conn_sqlite3 import *
        session = conn_sqlite3.make_session()
        a2 = User(name="uuuu")
        session.add(a2)
        session.commit()
    """

    def __init__(self):

        self.engine = create_engine('mysql+mysqlconnector://root:a3134402@localhost:3306/first')
        self.Base = declarative_base()

    def make_session(self):
        Session = sessionmaker(bind=self.engine)
        return Session()

    def make_table(self):

        Base = self.Base.metadata.create_all(self.engine)
        return Base




conn_sqlite3 = ConnectSqlite3()
BASE = conn_sqlite3.Base


class Base(BASE):
    __tablename__ = 'gupiao'
    id = Column(Integer, primary_key=True, autoincrement=True)

    code = Column(Integer, index=True)
    name = Column(String(30))
    date = Column(String(20))
    kp = Column(Float)
    zg = Column(Float)
    zd = Column(Float)
    sp = Column(Float)
    today20 = Column(Float, nullable=True)
    today_md = Column(Float, nullable=True)
    today_bls = Column(Float, nullable=True)
    today_blz = Column(Float, nullable=True)
    today_blx = Column(Float, nullable=True)
    today_ma2011 = Column(Float, nullable=True)
    today_md11 = Column(Float, nullable=True)
    today_bls11 = Column(Float, nullable=True)
    today_blz11 = Column(Float, nullable=True)
    today_blx11 = Column(Float, nullable=True)
    __table_args__ = (
        UniqueConstraint('code', 'name', 'date', name='uix_code_name_date'),

    )

# conn_sqlite3.make_table()
# session = conn_sqlite3.make_session()



