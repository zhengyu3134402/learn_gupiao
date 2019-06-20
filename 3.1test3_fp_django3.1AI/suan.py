import os
import re
import time
from sqlalchemy import Column, Integer, String, Float, UniqueConstraint
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import openpyxl

DB_NAME = 'mysql+mysqlconnector://root:a3134402@localhost:3306/testai1'
BASE = declarative_base()

class A(BASE):
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

class TakeFilePlace:

    def __init__(self):
        self.work_list_path = os.getcwd()+'\\export\\'
        self.work_list_filename_list = os.listdir(self.work_list_path)


def del_test4_gupiao_avg():
    import pymysql
    from pymysql.err import InternalError
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='a3134402', db='testai2')

    cursor = conn.cursor()

    try:
        cursor.execute("drop table gupiao_avg")  # 执行原生sql语句
    except InternalError:
        cursor.close()

        conn.close()

    else:
        cursor.close()

        conn.close()

def compute_final_result(r2):

    result_li = []  # 计算结果存储列表

    three0_days = []  # 31天数据存储列表

    flag_day = 0  # 天数标杆
    for i in r2:

        flag_day += 1  # 因为需要大前天的数据所以从第4天开始算起

        if len(three0_days) != 0:

            if i.code == three0_days[-1].code:  # 如果r2表中的股票代码等于30天列表的的代码

                three0_days.append(i)  # 将前31天数据加入列表

                if flag_day == 35:
                    compute_after_20_result(three0_days)

                elif flag_day > 35:

                    three0_days.pop(0)  # 删除第一天的值是列表保持4天的数据值

                    compute_after_20_result(three0_days)


            elif i.code != three0_days[-1].code:  # 如果r2表中的股票代码不等于30天列表的的代码

                three0_days = []
                flag_day = 0
        elif len(three0_days) == 0:

            three0_days.append(i)

    # return result_li



def computed_avg(flag_value_list):

    return sum(flag_value_list)/len(flag_value_list)

def put_data_in_mysql(all_list):
    from conndatabase1 import ConnectMysql

    conn = ConnectMysql()
    session = conn.session
    session.add(all_list)
    session.commit()
    session.close()

def write_infomation_to_mysql(result_list,make_b_name):
    from conndatabase2 import C

    one_result_list = []
    flag_num = 0
    for five_day_obj in result_list:

        result0 = five_day_obj[0]  # 昨日
        result1 = five_day_obj[1]  # 当天
        result2 = five_day_obj[2]  # 第一日
        result3 = five_day_obj[3]  # 第二日
        result4 = five_day_obj[4]  # 第三日
        result5 = five_day_obj[5]  # 第四日
        result6 = five_day_obj[6]  # 第五日

        kp0, zg0, zd0, sp0 = result0.kp, result0.zg, result0.zd, result0.sp
        kp1, zg1, zd1, sp1 = result1.kp, result1.zg, result1.zd, result1.sp
        kp2, zg2, zd2, sp2 = result2.kp, result2.zg, result2.zd, result2.sp
        kp3, zg3, zd3, sp3 = result3.kp, result3.zg, result3.zd, result3.sp
        kp4, zg4, zd4, sp4 = result4.kp, result4.zg, result4.zd, result4.sp
        kp5, zg5, zd5, sp5 = result5.kp, result5.zg, result5.zd, result5.sp
        kp6, zg6, zd6, sp6 = result6.kp, result6.zg, result6.zd, result6.sp

        kp2_sp0 = round(sp2 / sp0, 5)
        # print(sp2, kp0, sp2 / sp0)

        kp2_sp1 = str(round(kp2 / sp1, 5))
        zg2_sp1 = str(round(zg2 / sp1, 5))
        zd2_sp1 = str(round(zd2 / sp1, 5))
        sp2_sp1 = str(round(sp2 / sp1, 5))

        kp3_sp1 = str(round(kp3 / sp1, 5))
        zg3_sp1 = str(round(zg3 / sp1, 5))
        zd3_sp1 = str(round(zd3 / sp1, 5))
        sp3_sp1 = str(round(sp3 / sp1, 5))

        kp4_sp1 = str(round(kp4 / sp1, 5))
        zg4_sp1 = str(round(zg4 / sp1, 5))
        zd4_sp1 = str(round(zd4 / sp1, 5))
        sp4_sp1 = str(round(sp4 / sp1, 5))

        kp5_sp1 = str(round(kp5 / sp1, 5))
        zg5_sp1 = str(round(zg5 / sp1, 5))
        zd5_sp1 = str(round(zd5 / sp1, 5))
        sp5_sp1 = str(round(sp5 / sp1, 5))

        kp6_sp1 = str(round(kp6 / sp1, 5))
        zg6_sp1 = str(round(zg6 / sp1, 5))
        zd6_sp1 = str(round(zd6 / sp1, 5))
        sp6_sp1 = str(round(sp6 / sp1, 5))
        make_c = C(args_name=make_b_name, code=str(result1.code), name=result1.name,
                   date=result1.date, kp2_sp0=kp2_sp0, kp2_sp1=kp2_sp1, zg2_sp1=zg2_sp1,
                   zd2_sp1=zd2_sp1, sp2_sp1=sp2_sp1, kp3_sp1=kp3_sp1, zg3_sp1=zg3_sp1,
                   zd3_sp1=zd3_sp1, sp3_sp1=sp3_sp1, kp4_sp1=kp4_sp1, zg4_sp1=zg4_sp1,
                   zd4_sp1=zd4_sp1, sp4_sp1=sp4_sp1, kp5_sp1=kp5_sp1, zg5_sp1=zg5_sp1,
                   zd5_sp1=zd5_sp1, sp5_sp1=sp5_sp1, kp6_sp1=kp6_sp1, zg6_sp1=zg6_sp1,
                   zd6_sp1=zd6_sp1, sp6_sp1=sp6_sp1)
        try:
            put_info_in_mysql(make_c)
        except:
            print('haha')

def put_info_in_mysql(make_c):
    from conndatabase2 import ConnectMysql

    conn = ConnectMysql()
    session = conn.session
    try:
        session.add(make_c)
    except:
        pass
    session.commit()
    session.close()



def conn_mysql(code):

    engine = create_engine(DB_NAME)
    Session = sessionmaker(bind=engine)
    session = Session()
    all_data = list(session.query(A).filter_by(code=int(code.strip())))
    session.close()
    return all_data

















def compute_after_20_result(four_days):
    # 【-10】大大前天
    # 【-9】大前天
    # 【-8】前天
    # 【-7】昨日
    # 【-6】当天
    # 【-5】次日
    # 【-4】第二日
    # 【-3】第三日
    # 【-2】第四日
    # 【-1】第五日
    from conndatabase1 import B

    result_list = []
    import itertools
    # 修改4--------------------------------------------------------------------------------
    a = [x/100 for x in range(90, 111)]
    b = [x/100 for x in range(90, 111)] # 请修改蓝字的地方 篮子的地方为指标的范围*100 定义号变量不要重复
    # 修改4--------------------------------------------------------------------------------

    # 修改2--------------------------------------------------------------------------------
    for j, k in itertools.product(a, b):    # 上面修改4中有什么变量就往括号中填什么变量
    # 修改2--------------------------------------------------------------------------------

        # 修改1--------------------------------------------------------------------------------
        if (j-0.01)<=four_days[-6].sp / four_days[-7].sp <= j and (k-0.01)<=four_days[-7].sp/four_days[-8].sp <= k:


        # 修改1--------------------------------------------------------------------------------

            datas = four_days[-5].sp/four_days[-6].sp

            # 修改3--------------------------------------------------------------------------------
            make_b = B(name='j%r,k%r' % (j, k), sp2_sp1=datas) # 改绿字的地方和括号中的变量 修改2中有设么变量 绿字就填写什么变量 xx%r
            # 修改3--------------------------------------------------------------------------------

            check_result_list = [four_days[-7], four_days[-6], four_days[-5],
                               four_days[-4], four_days[-3], four_days[-2],
                               four_days[-1]]
            if not check_result_list in result_list:

                result_list.append(check_result_list)
            else:
                pass
            write_infomation_to_mysql(result_list, make_b.name)


            put_data_in_mysql(make_b)
            # print('j%r,k%r'%(j, k), datas)
        else:
            # print('haha')
            pass
# ===============================================================




































if __name__ == '__main__':

    t1 = time.time()
    with open(os.getcwd()+'\\code.txt', 'r')as f:
        for code in f:
            print(code)
            data = conn_mysql(code)
            # print(len(data))
            compute_final_result(data)

    # compute_finall_result_fff()
    t2 = time.time()
    print('共用了%r秒'%(t2-t1))
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    print('--------数据计算完毕，请查看test.xlsx表格----------')
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

    # import time
    # from multiprocessing import Pool
    #
    # del_test4_gupiao_avg()
    # t1 = time.time()
    # p = Pool(5)
    # flag = 0
    # with open(os.getcwd()+'\\code.txt', 'r')as f:
    #     for code in f:
    #
    #
    #         result = p.apply_async(conn_mysql, args=(code,), callback=compute_final_result)
    #
    #     p.close()
    #     p.join()
    #
    #     t2 = time.time()
    #
    #
    #     print('计算数据使用了=>', t2-t1, '秒')
    #
    #
    #     compute_finall_result_fff()
    #
    #
    #     print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    #     print('--------数据计算完毕，请查看test.xlsx表格----------')
    #     print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')










