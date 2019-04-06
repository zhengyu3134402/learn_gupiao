from sqlalchemy import Column, Integer, String,Float
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DB_NAME1 = 'mysql+mysqlconnector://root:a3134402@localhost:3306/testai2'
BASE1 = declarative_base()

class ConnectMysql:
    def __init__(self):
        self.engine = create_engine(DB_NAME1)
        self.create_table = BASE1.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

class B(BASE1):
    __tablename__ = 'gupiao_avg'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    sp2_sp1 = Column(Float)

