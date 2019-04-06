from sqlalchemy import Column, Integer, String,Float, UniqueConstraint
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import openpyxl
import os

DB_NAME1 = 'mysql+mysqlconnector://root:a3134402@localhost:3306/testai3'
BASE1 = declarative_base()

def make_excel():

    filepath = os.getcwd() + '\\test222.xlsx'
    wb = openpyxl.Workbook()
    wb.save(filepath)

def conn_mysql(code):

    engine = create_engine(DB_NAME1)
    Session = sessionmaker(bind=engine)
    session = Session()
    all_data = list(session.query(C).filter_by(code=int(code.strip())))
    session.close()
    return all_data


def write_to_excel(li):

    filepath = os.getcwd() + '\\test222.xlsx'
    wb = openpyxl.load_workbook(filepath)
    ws = wb.active
    data = ['技术指标参数', '代号', '名称', '日期', '次日收盘/昨日收盘', '次日开盘/当日收盘', '次日最高/当日收盘',
            '次日最低/当日收盘', '次日收盘/当日收盘', '第2日开盘/当日收盘', '第2日最高/当日收盘',
            '第2日最低/当日收盘', '第2日收盘/当日收盘', '第3日开盘/当日收盘', '第3日最高/当日收盘',
            '第3日最低/当日收盘', '第3日收盘/当日收盘', '第4日开盘/当日收盘', '第4日最高/当日收盘',
            '第4日最低/当日收盘', '第4日收盘/当日收盘', '第5日开盘/当日收盘', '第5日最高/当日收盘',
            '第5日最低/当日收盘', '第5日收盘/当日收盘']
    ws.append(data)
    for i in li:
        # print(i.args_name)
        ws.append([i.args_name, i.code, i.name, i.date, i.kp2_sp0, i.kp2_sp1,
                   i.zg2_sp1, i.zd2_sp1, i.sp2_sp1, i.kp3_sp1, i.zg3_sp1,
                   i.zd3_sp1, i.sp3_sp1, i.kp4_sp1, i.zg4_sp1, i.zd4_sp1,
                   i.sp4_sp1, i.kp5_sp1, i.zg5_sp1, i.zd5_sp1, i.sp5_sp1,
                   i.kp6_sp1, i.zg6_sp1, i.zd6_sp1, i.sp6_sp1])
    wb.save(filepath)



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

import time

t1 = time.time()
make_excel()

with open(os.getcwd() + '\\code.txt', 'r')as f:
    for code in f:
        print('正在把代码%r写入表格'%code)
        try:
            data = list(conn_mysql(code))
        except:
            pass
        else:
            write_to_excel(data)
t2 = time.time()

print('共用了%r秒'%(t2-t1))
print('|||||||||||||||||||||||||||||||||||||||||||||||||||')
print('--------写入表格完毕，请查看test222.xlsx表格----------')
print('|||||||||||||||||||||||||||||||||||||||||||||||||||')




# args_name ,code ,name,date ,kp2_sp0,kp2_sp1 ,zg2_sp1,zd2_sp1
# sp2_sp1,kp3_sp1 ,zg3_sp1 ,zd3_sp1 ,sp3_sp1 ,kp4_sp1 ,zg4_sp1
# zd4_sp1,sp4_sp1,kp5_sp1,zg5_sp1 ,zd5_sp1 ,sp5_sp1,kp6_sp1
# zg6_sp1,zd6_sp1,sp6_sp1