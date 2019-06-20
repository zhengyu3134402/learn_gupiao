import os
import openpyxl



def from_test4_take_data(flag):
    from conndatabase2 import ConnectMysql, C
    # print(flag)
    conn = ConnectMysql()
    session = conn.session
    print(flag)
    all_data = list(session.query(C).filter_by(args_name=flag))
    # print(all_data)
    session.close()
    return all_data


def computed_avg(flag_value_list):

    return sum(flag_value_list)/len(flag_value_list)


def write_to_excel(li):

    filepath = os.getcwd() + '\\test.xlsx'
    wb = openpyxl.load_workbook(filepath)
    ws = wb.active

    ws.append(li)
    wb.save(filepath)

def make_excel():

    filepath = os.getcwd() + '\\test.xlsx'
    wb = openpyxl.Workbook()
    wb.save(filepath)


def compute_finall_result_fff():
    import itertools
    make_excel()
    one_condition = []

    finall_result_dict = {}

    # 修改4--------------------------------------------------------------------------------
    a = [x / 100 for x in range(90, 111)]
    b = [x / 100 for x in range(90, 111)]  # 请修改蓝字的地方 篮子的地方为指标的范围*100 定义号变量不要重复
    # 修改4--------------------------------------------------------------------------------

    flag_value_list = []

    # 修改2--------------------------------------------------------------------------------
    for j, k in itertools.product(a, b):  # 上面修改4中有什么变量就往括号中填什么变量
    # 修改2--------------------------------------------------------------------------------

        # 修改3--------------------------------------------------------------------------------
        flag = 'j%r,k%r' % (j, k)      # 请修改绿字 xx%r   和后面括号中的变量 和上边呼应
        # 修改3--------------------------------------------------------------------------------
        all_flag_data = list(from_test4_take_data(flag))
        print(all_flag_data)
        if all_flag_data != []:
            for num in all_flag_data:
                flag_value_list.append(float(num.sp2_sp1))
            avg = computed_avg(flag_value_list)
            write_to_excel([flag, avg])
            flag_value_list.clear()

compute_finall_result_fff()