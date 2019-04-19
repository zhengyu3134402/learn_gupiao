import os
import re
from sqlalchemy import Column, Integer, String, Float, UniqueConstraint
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import openpyxl
write_to_file_result_list = []
DB_NAME = 'mysql+mysqlconnector://root:a3134402@localhost:3306/test2'
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









# 一起取


def write_result_to_file(result_list):
    # print(result)
    # ['600000', '浦发银行', '2006/10/10', 8.0, 0.95, 1.25, 0.85, 1.2, 1.2, 1.8, 1.1, 1.35, 1.3, 1.85, 1.2, 1.4, 1.45, 1.85,
    #  1.4, 1.65, 1.65, 1.65, 1.1, 1.25]
    with open(os.getcwd()+'\\result.txt', 'w')as f:
        for one_list in result_list:
            rep = re.sub(r',|\[|\]', r'\t', str(one_list))
            # print(rep)
            f.write(rep+'\n')



def compute_final_result(r2):

    result_li = []  # 计算结果存储列表

    three0_days = []  # 31天数据存储列表

    flag_day = 0  # 天数标杆
    for i in r2:
        # print(i)

        # count_time, '/', len(r2)# 可标记#############################################################3

        flag_day += 1  # 因为需要大前天的数据所以从第4天开始算起

        if len(three0_days) != 0:

            if i.code == three0_days[-1].code:  # 如果r2表中的股票代码等于30天列表的的代码

                three0_days.append(i)  # 将前31天数据加入列表

                if flag_day == 35:

                    result0, result1, result2, result3, result4, result5, result6 = compute_after_20_result(
                        three0_days)
                    # print(result1, result2, result3)
                    # print(result1, result2)
                    if result1:  # 如果存在查找结果
                        # print('55555555')
                        result_li.append(
                            (result0, result1, result2, result3, result4, result5, result6))  # 将查找结果加入到结果列表

                elif flag_day > 35:
                    # print('66666666')
                    three0_days.pop(0)  # 删除第一天的值是列表保持4天的数据值

                    result0, result1, result2, result3, result4, result5, result6 = compute_after_20_result(
                        three0_days)
                    # print(result1, result2,result3)
                    if result1:  # 如果存在查找结果
                        # print('7777777')
                        result_li.append(
                            (result0, result1, result2, result3, result4, result5, result6))  # 将查找结果加入到结果列表

            elif i.code != three0_days[-1].code:  # 如果r2表中的股票代码不等于30天列表的的代码

                three0_days = []
                flag_day = 0
        elif len(three0_days) == 0:

            three0_days.append(i)

    return result_li

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
    # print(four_days[-6].sp / four_days[-7].sp)
    # print(four_days[-7].sp / four_days[-8].sp)
    # print(four_days[-8].sp / four_days[-9].sp, four_days[-6].date)
    print(four_days[-6].code, four_days[-6].date)
    if 0.97<four_days[-6].sp / four_days[-7].sp<0.98 and \
        0.97<four_days[-7].sp / four_days[-8].sp<0.98 and \
         0.973 < four_days[-8].sp / four_days[-9].sp<0.974:

        #1.00,1.01|0.99,1.00|0.999,1.000|	0.993573333	3



        return four_days[-7], four_days[-6], four_days[-5], four_days[-4], four_days[-3], four_days[-2], four_days[
            -1]  # 别碰这一行

    else:

        return 0, 0, 0, 0, 0, 0, 0







def main(all_data):

    result = compute_final_result(all_data)
    # [({0}, {1}, {2}, {3}, {4},{5}), ({0}, {1}, {2}, {3}, {4}), ({0}, {1}, {2}, {3}, {4}), ({0}, {1}, {2}, {3}, {4}),({0}, {1}, {2}, {3}, {4})]
    one_result_list = []

    make_excel()

    if result != []:
        for five_day_obj in result:

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

            kp2_sp1 = round(kp2 / sp1, 5)
            zg2_sp1 = round(zg2 / sp1, 5)
            zd2_sp1 = round(zd2 / sp1, 5)
            sp2_sp1 = round(sp2 / sp1, 5)

            kp3_sp1 = round(kp3 / sp1, 5)
            zg3_sp1 = round(zg3 / sp1, 5)
            zd3_sp1 = round(zd3 / sp1, 5)
            sp3_sp1 = round(sp3 / sp1, 5)

            kp4_sp1 = round(kp4 / sp1, 5)
            zg4_sp1 = round(zg4 / sp1, 5)
            zd4_sp1 = round(zd4 / sp1, 5)
            sp4_sp1 = round(sp4 / sp1, 5)

            kp5_sp1 = round(kp5 / sp1, 5)
            zg5_sp1 = round(zg5 / sp1, 5)
            zd5_sp1 = round(zd5 / sp1, 5)
            sp5_sp1 = round(sp5 / sp1, 5)

            kp6_sp1 = round(kp6 / sp1, 5)
            zg6_sp1 = round(zg6 / sp1, 5)
            zd6_sp1 = round(zd6 / sp1, 5)
            sp6_sp1 = round(sp6 / sp1, 5)
            one_result_list.append([result1.code, result1.name, result1.date, kp2_sp0, kp2_sp1,
                                              zg2_sp1, zd2_sp1, sp2_sp1, kp3_sp1, zg3_sp1, zd3_sp1, sp3_sp1, kp4_sp1,
                                              zg4_sp1, zd4_sp1, sp4_sp1, kp5_sp1, zg5_sp1, zd5_sp1, sp5_sp1, kp6_sp1,
                                              zg6_sp1, zd6_sp1, sp6_sp1])

        write_to_file_result_list.append(one_result_list)

        write_to_excel(write_to_file_result_list)


def conn_mysql(code):

    engine = create_engine(DB_NAME)
    Session = sessionmaker(bind=engine)
    session = Session()
    all_data = list(session.query(A).filter_by(code=int(code.strip())))
    session.close()
    return all_data

def make_excel():

    filepath = os.getcwd() + '\\test.xlsx'
    wb = openpyxl.Workbook()
    wb.save(filepath)

def write_to_excel(li):

    filepath = os.getcwd() + '\\test.xlsx'
    wb = openpyxl.load_workbook(filepath)
    ws = wb.active
    data = ['代号', '名称', '日期', '次日收盘/昨日收盘', '次日开盘/当日收盘', '次日最高/当日收盘',
            '次日最低/当日收盘', '次日收盘/当日收盘', '第2日开盘/当日收盘', '第2日最高/当日收盘',
            '第2日最低/当日收盘', '第2日收盘/当日收盘', '第3日开盘/当日收盘', '第3日最高/当日收盘',
            '第3日最低/当日收盘', '第3日收盘/当日收盘', '第4日开盘/当日收盘', '第4日最高/当日收盘',
            '第4日最低/当日收盘', '第4日收盘/当日收盘', '第5日开盘/当日收盘', '第5日最高/当日收盘',
            '第5日最低/当日收盘', '第5日收盘/当日收盘']
    ws.append(data)
    for i in li:
        for j in i:
            ws.append(j)
    wb.save(filepath)

if __name__ == '__main__':
    import time
    from multiprocessing import Pool
    t1 = time.time()
    p = Pool(5)
    flag = 0
    with open(os.getcwd()+'\\code.txt', 'r')as f:
        for code in f:
            # print(code)

            result = p.apply_async(conn_mysql, args=(code,), callback=main)

        p.close()
        p.join()

        t2 = time.time()
        print(t2-t1)
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        print('--------数据计算完毕，请查看test.xlsx表格----------')
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')










