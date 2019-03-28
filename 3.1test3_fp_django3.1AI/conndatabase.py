from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DB_NAME = 'mysql+mysqlconnector://zhengyu:3134402@localhost:3306/test2'
BASE = declarative_base()


class A(BASE):
    __tablename__ = 'gupiao'
    id = Column(Integer, primary_key=True, autoincrement=True)

    code = Column(Integer)
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





db_name = 'mysql+mysqlconnector://zhengyu:3134402@localhost:3306/test2'
Base = declarative_base()
engine = create_engine(db_name)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
session.close()