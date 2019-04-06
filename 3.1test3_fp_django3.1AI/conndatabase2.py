from sqlalchemy import Column, Integer, String,Float, UniqueConstraint
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DB_NAME1 = 'mysql+mysqlconnector://root:a3134402@localhost:3306/testai3'
BASE1 = declarative_base()

class ConnectMysql:
    def __init__(self):
        self.engine = create_engine(DB_NAME1)
        self.create_table = BASE1.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

class C(BASE1):
    __tablename__ = 'gupiao_info'
    id = Column(Integer, primary_key=True, autoincrement=True)

    args_name = Column(String(100))
    code = Column(String(20))
    name = Column(String(20))
    date = Column(String(20))

    kp2_sp0 = Column(String(20))
    kp2_sp1 = Column(String(20))
    zg2_sp1 = Column(String(20))
    zd2_sp1 = Column(String(20))
    sp2_sp1 = Column(String(20))
    kp3_sp1 = Column(String(20))
    zg3_sp1 = Column(String(20))
    zd3_sp1 = Column(String(20))
    sp3_sp1 = Column(String(20))
    kp4_sp1 = Column(String(20))
    zg4_sp1 = Column(String(20))
    zd4_sp1 = Column(String(20))
    sp4_sp1 = Column(String(20))
    kp5_sp1 = Column(String(20))
    zg5_sp1 = Column(String(20))
    zd5_sp1 = Column(String(20))
    sp5_sp1 = Column(String(20))
    kp6_sp1 = Column(String(20))
    zg6_sp1 = Column(String(20))
    zd6_sp1 = Column(String(20))
    sp6_sp1 = Column(String(20))
    __table_args__ = (
        UniqueConstraint('args_name', 'code', 'name', 'date', name='uix_args_code_name_date'),

    )