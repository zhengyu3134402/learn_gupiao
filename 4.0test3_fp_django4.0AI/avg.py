import time
import openpyxl
from lib.second_conn_sqlite3 import *


def from_database2_take_data(clear_name):



    session = second_conn_sqlite3.make_session()

    all_data = list(session.query(Second).filter_by(name=clear_name))
    write_to_excel(all_data, clear_name)
    session.close()




def write_to_excel(all_data, clear_name):

    avg_list = []

    filepath = os.getcwd() + '\\avg.xlsx'
    wb = openpyxl.load_workbook(filepath)
    ws = wb.active
    for obj in all_data:

        avg_list.append(obj.sp2_sp1)

    ws.append([clear_name, sum(avg_list)/len(avg_list), len(avg_list)])
    wb.save(filepath)

def make_excel():

    filepath = os.getcwd() + '\\avg.xlsx'
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['技术指标', '平均数', '个数'])
    wb.save(filepath)


# def compute_finall_result_fff():



    # import itertools
    # make_excel()
    # one_condition = []
    #
    # finall_result_dict = {}
    #
    # # 修改4--------------------------------------------------------------------------------
    # a = [x / 100 for x in range(90, 111)]
    # b = [x / 100 for x in range(90, 111)]  # 请修改蓝字的地方 篮子的地方为指标的范围*100 定义号变量不要重复
    # # 修改4--------------------------------------------------------------------------------
    #
    # flag_value_list = []
    #
    # # 修改2--------------------------------------------------------------------------------
    # for j, k in itertools.product(a, b):  # 上面修改4中有什么变量就往括号中填什么变量
    # # 修改2--------------------------------------------------------------------------------
    #
    #     # 修改3--------------------------------------------------------------------------------
    #     flag = 'j%r,k%r' % (j, k)      # 请修改绿字 xx%r   和后面括号中的变量 和上边呼应
    #     # 修改3--------------------------------------------------------------------------------
    #     all_flag_data = list(from_test4_take_data(flag))
    #     print(all_flag_data)
    #     if all_flag_data != []:
    #         for num in all_flag_data:
    #             flag_value_list.append(float(num.sp2_sp1))
    #         avg = computed_avg(flag_value_list)
    #         write_to_excel([flag, avg])
    #         flag_value_list.clear()

# compute_finall_result_fff()

def computed_avg():
    with open('jishuzhibiao.txt', 'r') as f:

        s = f.readlines()
        for name in s:
            clear_name = name.strip()
            from_database2_take_data(clear_name)

t1 = time.time()
make_excel()
computed_avg()
t2 = time.time()


result_time = t2-t1

print(';;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;')
print('总共花了%r秒, 请查看avg.xlsx表格！！'%(result_time))
print(';;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;')
