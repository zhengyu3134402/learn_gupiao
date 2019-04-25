
import time
from lib.base_conn_sqlite3 import *
from lib.second_conn_sqlite3 import *

class TakeFilePlace:

    def __init__(self):
        self.work_list_path = os.getcwd()+'\\export\\'
        self.work_list_filename_list = os.listdir(self.work_list_path)




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

    # ============================================
    a = four_days[-6].today_blx / four_days[-7].today_blx -four_days[-7].today_blx / four_days[-8].today_blx

    if four_days[-6].today_blx / four_days[-7].today_blx > 1:
    # ============================================
    # 0.91~1.10 : %s
    # 0.990~1.110 %st

        datas = four_days[-5].sp / four_days[-6].sp  # 次日除以今日
        print(four_days[-6].code, four_days[-6].date)
        # =========================================================

        sp2_sp0, kp2_sp1, zg2_sp1, zd2_sp1, sp2_sp1, kp3_sp1, zg3_sp1, zd3_sp1, sp3_sp1, kp4_sp1, \
        zg4_sp1, zd4_sp1, sp4_sp1, kp5_sp1, zg5_sp1, zd5_sp1, sp5_sp1, kp6_sp1, zg6_sp1, zd6_sp1, \
        sp6_sp1 = make_all_avg([four_days[-7], four_days[-6], four_days[-5], four_days[-4], four_days[-3], four_days[-2], four_days[-1]])
        # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
        make_s = Second(name='%s' % (str(a)), name1=four_days[-6].name, code=four_days[-6].code, date=four_days[-6].date,
                        sp2_sp0=sp2_sp0, kp2_sp1=kp2_sp1, zg2_sp1=zg2_sp1, zd2_sp1=zd2_sp1,
                        sp2_sp1=sp2_sp1, kp3_sp1=kp3_sp1, zg3_sp1=zg3_sp1, zd3_sp1=zd3_sp1,
                        sp3_sp1=sp3_sp1, kp4_sp1=kp4_sp1, zg4_sp1=zg4_sp1, zd4_sp1=zd4_sp1,
                        sp4_sp1=sp4_sp1, kp5_sp1=kp5_sp1, zg5_sp1=zg5_sp1, zd5_sp1=zd5_sp1,
                        sp5_sp1=sp5_sp1, kp6_sp1=kp6_sp1, zg6_sp1=zg6_sp1, zd6_sp1=zd6_sp1,
                        sp6_sp1=sp6_sp1)
        # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&



        put_computed_data_to_seconddb(make_s)

def make_all_avg(five_day_obj):
    if five_day_obj != []:


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

        sp2_sp0 = round(sp2 / sp0, 5)
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
        return sp2_sp0, kp2_sp1, zg2_sp1, zd2_sp1, sp2_sp1, kp3_sp1, zg3_sp1, zd3_sp1, \
               sp3_sp1, kp4_sp1, zg4_sp1, zd4_sp1, sp4_sp1, kp5_sp1, zg5_sp1, zd5_sp1, \
               sp5_sp1, kp6_sp1, zg6_sp1, zd6_sp1, sp6_sp1



jishuzhibiao_name_list = set()  # 为了以后实现多线程，如果不用多线程直接写入文本也可


def make_solt(make_s):

    num = ''

    if ',' in make_s.name:

        name_list = make_s.name.split(',')



        for num1 in name_list:

            if 't' in num1:

                new_num1 = num1[0:-1]
                # print(len(new_num1))
                # print(new_num1) # new_num1[0:5]
                num += ((str(new_num1[0:5])+'0000')[0:5])  + ',' + ((str(float(new_num1)+0.001)+'0000')[0:5]) +'|'
                # print(num)
            else:
                num += ((str(num1[0:4])+'0000')[0:4]) + ',' + ((str(float(num1)+0.01)+'0000')[0:4]) + '|'
        # print(num)
        jishuzhibiao_name_list.add(num)
        make_s.name = num
        # print(jishuzhibiao_name_list)

        return make_s

    else:
        if 'q' in make_s.name:
            new_num1 = make_s.name[0:-1]
            num1_range = (new_num1 + '0000')[0:5] + ',' + (str(float(new_num1) + 0.001) + '0000')[0:5]  # 不四舍五入取小数点后面2位  不四舍五入小数点后两位+0.01  取名
            # print(num1_range)
            jishuzhibiao_name_list.add(num1_range)
            make_s.name = num1_range
            return make_s

        elif 'w' in make_s.name:
            new_num1 = make_s.name[0:-1]
            num1_range = (new_num1 + '00000')[0:6] + ',' + (str(float(new_num1) + 0.0001) + '00000')[0:6]  # 不四舍五入取小数点后面2位  不四舍五入小数点后两位+0.01  取名
            # print(num1_range)
            jishuzhibiao_name_list.add(num1_range)
            make_s.name = num1_range
            return make_s

        else:
            num1 = make_s.name[0:4]
            num1_range = (num1+'0000')[0:4] + ',' + (str(float(num1)+0.01)+'0000')[0:4]  # 不四舍五入取小数点后面2位  不四舍五入小数点后两位+0.01  取名
            # print(num1_range)
            jishuzhibiao_name_list.add(num1_range)
            make_s.name = num1_range
            return make_s



def put_computed_data_to_seconddb(make_s):
    new_make_s = make_solt(make_s)
    session2 = second_conn_sqlite3.make_session()
    session2.add(new_make_s)
    session2.commit()
    session2.close()





def conn_mysql(code):
    session = conn_sqlite3.make_session()
    all_data = list(session.query(Base).filter_by(code=int(code.strip())))
    session.close()
    return all_data










def main(all_data):

    compute_final_result(all_data)


if __name__ == '__main__':


    # #单线程===============================================
    # t1 = time.time()
    # with open(os.getcwd()+'\\code.txt', 'r')as f:
    #     for code in f:
    #         print(code)
    #         data = conn_mysql(code)
    #         # print(len(data))
    #         compute_final_result(data)
    #
    # # compute_finall_result_fff()
    # with open('jishuzhibiao.txt', 'w') as f:
    #     for i in jishuzhibiao_name_list:
    #         f.write(i+'\n')
    # t2 = time.time()
    # print('共用了%r秒'%(t2-t1))
    # print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    # print('--------数据计算完毕，请查看test.xlsx表格----------')
    # print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    # #单线程===============================================

    # 多进程================================================
    # import time
    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    os.system('python del_datebase2.py')
    os.system('python 03_创建第二次结果数据库表.py')
    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    from multiprocessing import Pool

    t1 = time.time()



    p = Pool(5)

    with open(os.getcwd()+'\\code.txt', 'r')as f:

        for code in f:
            print(code)

            result = p.apply_async(conn_mysql, args=(code,), callback=main)

        p.close()
        p.join()

    with open('jishuzhibiao.txt', 'w') as f:
        for i in jishuzhibiao_name_list:
            f.write(i+'\n')

    t2 = time.time()
    #
    #
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    print('计算数据使用了=>', t2-t1, '秒', '=>正在计算平均数请稍等.......')
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    os.system('python avg.py')
    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    # # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    os.system('python zuizong.py')
    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    # 此处为程序执行完成之后自动关机（如果想执行，请删除前面的 ‘#’ 号）================
    #os.system('shutdown -s -t 0')
    # 此处为程序执行完成之后自动关机（如果想执行，请删除前面的 ‘#’ 号）================









