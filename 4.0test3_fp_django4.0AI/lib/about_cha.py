import os
import decimal
import math
import time
import copy

from sqlalchemy.exc import IntegrityError
from sqlalchemy import Column, Integer, String, Float, UniqueConstraint, Index
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .base_conn_sqlite3 import *
# DB_NAME = 'mysql+mysqlconnector://root:a3134402@localhost:3306/testai1'
# BASE = declarative_base()
# 11
# class A(BASE):
#     __tablename__ = 'gupiao'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#
#     code = Column(Integer, index=True)
#     name = Column(String(30))
#     date = Column(String(20))
#     kp = Column(Float)
#     zg = Column(Float)
#     zd = Column(Float)
#     sp = Column(Float)
#     today20 = Column(Float, nullable=True)
#     today_md = Column(Float, nullable=True)
#     today_bls = Column(Float, nullable=True)
#     today_blz = Column(Float, nullable=True)
#     today_blx = Column(Float, nullable=True)
#     today_ma2011 = Column(Float, nullable=True)
#     today_md11 = Column(Float, nullable=True)
#     today_bls11 = Column(Float, nullable=True)
#     today_blz11 = Column(Float, nullable=True)
#     today_blx11 = Column(Float, nullable=True)
#     __table_args__ = (
#         UniqueConstraint('code', 'name', 'date', name='uix_code_name_date'),
#
#     )

# class ConnectMysql:
#     def __init__(self):
#         self.engine = create_engine(DB_NAME)
#         self.create_table = BASE.metadata.create_all(self.engine)
#         self.session = sessionmaker(bind=self.engine)()

class Compute_boll:
    '''
    计算布林线
    '''
    def __init__(self, sp_20_list):
        self.sp_20_list = sp_20_list
        self.today_ma20 = decimal.Decimal(self.compute_ma20())
        self.today_md = decimal.Decimal(self.compute_md())
        self.blz = decimal.Decimal(self.compute_today_boll_center_line())
        self.bls = decimal.Decimal(self.compute_today_boll_up_line())
        self.blx = decimal.Decimal(self.compute_today_boll_down_line())
        self.sp_20_list_1_1 = self.make_sp_20_list_1_1()
        self.today_ma20_1_1 = decimal.Decimal(self.compute_ma20_1_1())
        self.today_md_1_1 = decimal.Decimal(self.compute_md_1_1())
        self.blz_1_1 = decimal.Decimal(self.compute_today_boll_center_line_1_1())
        self.bls_1_1 = decimal.Decimal(self.compute_today_boll_up_line_1_1())
        self.blx_1_1 = decimal.Decimal(self.compute_today_boll_down_line_1_1())

    def make_sp_20_list_1_1(self):

        sp_20_list_1_1 = copy.deepcopy(self.sp_20_list)
        sp_20_list_1_1[-1] = sp_20_list_1_1[-2]*decimal.Decimal(1.1)
        return sp_20_list_1_1

    def compute_ma20_1_1(self):

        return sum(self.sp_20_list_1_1)/20

    def compute_ma20(self):
        return sum(self.sp_20_list) / 20

    def compute_md_1_1(self):
        everyday_ma20_1_1_mdlist = []

        for sp in self.sp_20_list_1_1:  # 对20日收盘价循环
            everyday_ma20_1_1_mdlist.append((decimal.Decimal(sp) - self.today_ma20_1_1) ** 2)  # 将 (每日收盘-ma2)**2 加入到列表
        md_1_1 = math.sqrt(sum(everyday_ma20_1_1_mdlist) / 19)  # 求md

        return md_1_1

    def compute_md(self):
        '''
        MD = sqrt(sum((当天收盘价 - MA20) ** 2 + ...) / 19)
        '''
        everyday_ma20_mdlist=[]
        for sp in self.sp_20_list:  # 对20日收盘价循环
            everyday_ma20_mdlist.append((decimal.Decimal(sp) - self.today_ma20) ** 2)  # 将 (每日收盘-ma2)**2 加入到列表
        md = math.sqrt(sum(everyday_ma20_mdlist) / 19)  # 求md

        return md

    def compute_today_boll_down_line(self):
        return self.blz-2*self.today_md

    def compute_today_boll_down_line_1_1(self):
        return self.blz_1_1-2*self.today_md_1_1

    def compute_today_boll_center_line(self):

        return self.today_ma20

    def compute_today_boll_center_line_1_1(self):
        return self.today_ma20_1_1

    def compute_today_boll_up_line(self):
        return self.blz+2*self.today_md

    def compute_today_boll_up_line_1_1(self):
        return self.blz_1_1+2*self.today_md_1_1


class Dofile:     # 创建处理文件类

    def __init__(self):         # 初始化类
        self.workfile_position = os.getcwd() + '\\export\\'  # 初始化执行文件目录位置
        self.file_list = self.get_update_filelist()     # 初始化执行文件列表
        self.count_file_flag = 0   # 初始化计数操作标杆为空列表
        self.file_num = len(self.file_list)  # 初始化处理文件的个数
        self.code = None
        self.name = None
        self.date = None
        self.kp = None
        self.zg = None
        self.zd = None
        self.sp = None
        self.today20 = None
        self.today_md = None
        self.today_bls = None
        self.today_blz = None
        self.today_blx = None
        self.today_ma2011 = None
        self.today_md11 = None
        self.today_bls11 = None
        self.today_blz11 = None
        self.today_blx11 = None
        self.one_file_data = None

    def get_update_filelist(self):
        """获取上传目录文件列表"""
        file_list = os.listdir(self.workfile_position)
        return file_list

    # def delete_file(self):
    #     '''删除export目录中的所有文件'''
    #     for i in self.file_list:
    #         os.remove(self.workfile_position+'\\'+i)

    def read_file_lines(self,file):
        '''读取文件每行内容'''
        with open(self.workfile_position + '/' + file, "r", encoding="GBK")as f:  # 打开目录文件
            data_list = f.readlines()  # 将单个文件内容按行分割放到列表中
        data_list.pop()  # 删除头部无用内容
        data_list.pop(1)  # 删除尾部无用内容
        return data_list

    def take_code_name(self, lines_list):
        '''提取文件中的code和name'''

        head = lines_list[0].strip()  # 对去除两端的换行符
        ret = head.split(" ")  # 对herd变量的内容按空格进行分割
        code = ret[0]  # 获取代号
        name = ret[1]  # 获取名字
        return code, name

    def take_date_kp_zg_zd_cjl_cje(self, one_day_info):
        '''提取文件中的kp，zg，zd，cjl，cje'''
        one_day_info.strip()  # 去除两端换行符

        one_day_info_list = one_day_info.split("\t")  # 按制表符进行分割

        if decimal.Decimal(one_day_info_list[1]) <= 0 or decimal.Decimal(one_day_info_list[2]) <= 0 or\
                decimal.Decimal(one_day_info_list[3]) <= 0 or decimal.Decimal(one_day_info_list[4]) <= 0:

            pass  # 对文件内容进行过滤 kp sp zg zd 的值其中有一个小于或等于零则不写入
        else:  # 如果满足kp sp zg zd 的值其中有一个不小于或等于零得条件

            return one_day_info_list[0], one_day_info_list[1], one_day_info_list[2],\
                   one_day_info_list[3], one_day_info_list[4], one_day_info_list[5],\
                   one_day_info_list[6].strip()


    def take_data(self):
        """提取文件主要内容,并向数据库中批量插入数据"""



        code_list = []
        line_all_list = []
        all_list = []
        flag_file = 0
        quotient, remainder = self.computed_num(len(self.file_list))
        flag_quotient = 0



        for file in self.file_list:     # 循环目录文件
            ta = time.time()
            print(file)
            self.one_file_data = None
            data_all_list = []          # 创建批量加入数据库的列表
            sp_20_list = []
            lines_list = self.read_file_lines(file)
            if len(lines_list) <= 3: # 如果数据为空不插入停止本次循环，继续下次循环
                continue
            self.code, self.name = self.take_code_name(lines_list)

            code_list.append(self.code)

            for info in lines_list[1:]:

                return_value = self.take_date_kp_zg_zd_cjl_cje(info)

                if return_value != None:

                    self.date, self.kp, self.zg, self.zd, self.sp, cjl, cje = self.take_date_kp_zg_zd_cjl_cje(info)
                    sp_20_list.append(decimal.Decimal(self.sp))


                    if len(sp_20_list) >= 20:

                        self.today_ma20, self.today_md, self.today_bls, self.today_blz, self.today_blx, self.today_ma2011,\
                        self.today_md11, self.today_bls11,self.today_blz11,\
                        self.today_blx11 = self.take_ma20_md_bollup_bollcenter_bolldown(sp_20_list)
                        make_obj = Base(code=self.code, name=self.name, date=self.date, kp=float(self.kp), zg=float(self.zg),
                                        zd=float(self.zd), sp=float(self.sp), today20=self.today_ma20,
                                        today_md=self.today_md, today_bls=self.today_bls, today_blz=self.today_blz,
                                        today_blx=self.today_blx, today_ma2011=self.today_ma2011,
                                        today_md11=self.today_md11, today_bls11=self.today_bls11,
                                        today_blz11=self.today_blz11, today_blx11=self.today_blx11)


                        all_list.append(make_obj)
                    else:

                        make_obj = Base(code=self.code, name=self.name, date=self.date, kp=float(self.kp), zg=float(self.zg),
                                        zd=float(self.zd), sp=float(self.sp))

                        all_list.append(make_obj)
            tb = time.time()

            print(tb-ta)
            flag_file += 1
            flag_quotient += 1
            if flag_file == 10:
                try:
                    self.put_data_in_mysql(all_list)
                except IntegrityError:
                    print('出现错误：未清空数据，请先清空数据，在插入数据')
                all_list = []
                flag_file = 0
            elif flag_quotient >= 10*quotient:
                self.put_data_in_mysql(all_list)
            # try:
            #     self.put_data_in_mysql(data_all_list)
            # except IntegrityError:
            #    print('数据已存在，不再此条信息，继续插入下一条')
        self.write_code_to_txt(code_list)
        print('**************************************************')
        print('%%%%%%%%%%%%%%%%%%插入数据完毕%%%%%%%%%%%%%%%')
        print('**************************************************')
    def computed_num(self, file_nums):
        """计算插入数据库文件数/10的商和余数"""
        return divmod(file_nums, 10)


    def write_code_to_txt(self, code_list):
        with open(os.getcwd()+'\\code.txt', 'w')as f:
            for i in code_list:
                f.write(i+'\n')

    # 插入数据的唯一性
    def put_data_in_mysql(self, all_list):
        session = conn_sqlite3.make_session()
        session.add_all(all_list)
        session.commit()
        session.close()

    # def write_data_all_list_to_result(self, date_all_list, file_name):
    #     with open(os.getcwd()+'\\result\\'+ file_name, 'w', encoding="GBK")as f:
    #         for line in date_all_list:
    #             f.write(str(line)+'\n')



    def take_ma20_md_bollup_bollcenter_bolldown(self, sp_20_list):
        '''根据数据计算出ma20和布林线'''
        new_sp_20_list = self.makesure_sp_list_20(sp_20_list)
        compute_boll = Compute_boll(new_sp_20_list)
        today_ma20 = round(float(compute_boll.today_ma20), 5)
        today_md = round(float(compute_boll.today_md), 5)
        today_bollup = round(float(compute_boll.bls), 5)
        today_bollcenter = round(float(compute_boll.blz), 5)
        today_bolldown = round(float(compute_boll.blx), 5)
        today_ma20_1_1 = round(float(compute_boll.today_ma20_1_1), 5)
        today_md_1_1 = round(float(compute_boll.today_md_1_1), 5)
        today_bollup_1_1 = round(float(compute_boll.bls_1_1), 5)
        today_bollcenter_1_1 = round(float(compute_boll.blz_1_1), 5)
        today_bolldown_1_1 = round(float(compute_boll.blx_1_1), 5)

        return today_ma20, today_md, today_bollup, today_bollcenter, today_bolldown, today_ma20_1_1, today_md_1_1,\
    today_bollup_1_1,today_bollcenter_1_1, today_bolldown_1_1

    def makesure_sp_list_20(self, sp_20_list):
        '''确保收盘列表长度为20'''

        if len(sp_20_list) == 20:
            return sp_20_list
        elif len(sp_20_list) >20:
            sp_20_list.pop(0)
            return sp_20_list

    def save_putindatabase_objcode(self, code_list):
        '''把插入到数据库中的对象code写入到obj_code.txt中'''

        with open(os.getcwd()+'\\test111\\obj_code.txt', 'w')as f:
            for obj_code in code_list:
                f.write(obj_code+'\n')


    def copy_codetxt_to_resulttxt(self):

        with open("code.txt", "r") as f1:
            f = f1.read()
            print(f)

        with open("result.txt", "w") as f2:
            f2.write(f)



def main():
    a = Dofile()
    a.take_data()


if __name__ == '__main__':
    main()






