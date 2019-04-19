from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer, Float, UniqueConstraint
import os




# SPATH = os.path.abspath(os.path.dirname(__file__))+'\\..\\db\\second.db'


class SecondConnectSqlite3:
    """
        在其他模块中的使用
        from second_conn_sqlite3 import *
        session2 = conn_sqlite3.make_session()
        a2 = User(name="uuuu")
        session.add(a2)
        session.commit()
    """

    def __init__(self):

        self.engine = create_engine('mysql+mysqlconnector://root:a3134402@localhost:3306/second')  # 连接
        self.Base = declarative_base()

    def make_session(self):
        Session = sessionmaker(bind=self.engine)
        return Session()

    def make_table(self):

        Base = self.Base.metadata.create_all(self.engine)
        return Base




second_conn_sqlite3 = SecondConnectSqlite3()
SBASE = second_conn_sqlite3.Base


class Second(SBASE):
    __tablename__ = 'gupiao_second'
    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String(100), index=True)
    code = Column(Integer)
    date = Column(String(20))

    sp2_sp0 = Column(Float)

    kp2_sp1 = Column(Float)
    zg2_sp1 = Column(Float)
    zd2_sp1 = Column(Float)
    sp2_sp1 = Column(Float)

    kp3_sp1 = Column(Float)
    zg3_sp1 = Column(Float)
    zd3_sp1 = Column(Float)
    sp3_sp1 = Column(Float)

    kp4_sp1 = Column(Float)
    zg4_sp1 = Column(Float)
    zd4_sp1 = Column(Float)
    sp4_sp1 = Column(Float)

    kp5_sp1 = Column(Float)
    zg5_sp1 = Column(Float)
    zd5_sp1 = Column(Float)
    sp5_sp1 = Column(Float)

    kp6_sp1 = Column(Float)
    zg6_sp1 = Column(Float)
    zd6_sp1 = Column(Float)
    sp6_sp1 = Column(Float)


    __table_args__ = (
        UniqueConstraint('code', 'name', 'date', name='uix_code_name_date'),

    )

# second_conn_sqlite3.make_table()
# session2 = second_conn_sqlite3.make_session()


