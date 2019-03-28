
import os

from django.shortcuts import render, HttpResponse

from yingyong1.models import Gupiao


def get_current_path():
    """获取当前脚本路径"""
    current_path = os.getcwd()
    # print(current_path)
    return current_path


def get_work_file(path):
    """将被执行工作文件夹添加到当前路径下,
    # 获被执行工作文件夹的绝对路径"""
    file_dir = os.path.join(path, "yingyong1/export")
    # print(file_dir)
    return file_dir


def get_work_file_list(work_file):
    """获取被执行目录文件列表"""

    work_file_list = os.listdir(work_file)
    return work_file_list


def put_data_in_database(work_file_list, work_file):
    """将数据插入到数据库中"""
    for file in work_file_list:
        try:
            print(file)
            take_data(file, work_file)
        except Exception as e:
            print(e)

def insert_data1(request):
    """批量向数据库中插入数据"""
    current_path = get_current_path()
    work_file = get_work_file(current_path)
    work_file_list = get_work_file_list(work_file)
    put_data_in_database(work_file_list, work_file)

    return HttpResponse('haha')


def take_data(file, work_file):
    """提取文件主要内容,并向数据库中批量插入数据"""
    import decimal
    with open(os.path.join(work_file, file), "r", encoding="GBK")as f:

        data_list = f.readlines()

    data_list.pop()
    data_list.pop(1)

    data_all_list = []

    head = data_list[0].strip()
    ret = head.split(" ")
    code = ret[0]
    name = ret[1]

    for i in data_list[1:]:

        i.strip()
        s = i.split("\t")

        if decimal.Decimal(s[1]) <= 0 or decimal.Decimal(s[2]) <= 0 or\
                decimal.Decimal(s[3]) <= 0 or decimal.Decimal(s[4]) <= 0:
            pass

        else:
            date = s[0]
            kp = s[1]
            zg = s[2]
            zd = s[3]
            sp = s[4]
            cjl = s[5]
            cje = s[6].strip()

            data_all_list.append(Gupiao(code=code, name=name, date=date, kp=kp, zg=zg,
                                        zd=zd, sp=sp, cjl=cjl, cje=cje))

    Gupiao.objects.bulk_create(data_all_list)


def search_boll(request):
    """查询布林线"""
    import time
    a = time.time()
    # print(a)
    time_li = []
    times = time.strftime("%H{y}%M{m}%S{s}").format(y='时', m='分', s='秒')
    # print(times)
    time_li.append(times)



    obj_list = Gupiao.objects.all()  # 获取所有数据
    r1 = obj_list.order_by("code", "date")  # 多个字段进行排序
    r2 = compute_boll(r1)   # 返回的是查询布林线

    final_result = compute_final_result(r2)  # 根据布林线结果计算最终结果

    # print(final_result)

    show_result_list = []
    # print(show_result_list)

    if final_result != []:

        for i in final_result:

            # [jintin,mingting]
            # [a,b,c,d]
            # print(final_result)
            # print(final_result[0][0].date,final_result[1][0].date,final_result[2][0].date)
            # result0 = i[-1][0]
            # print(len(final_result))

            print('000000',i[0][0].date)
            print('111111',i[1][0].date)
            print('222222',i[2][0].date)
            print('333333',i[3][0].date)
            print('444444', i[4][0].date)
            print('555555', i[5][0].date)
            #
            result0 = i[0][0]       # 昨日
            result1 = i[1][0]	    # 当天
            result2 = i[2][0]	    # 第一日
            result3 = i[3][0]       # 第二日
            result4 = i[4][0]       # 第三日
            result5 = i[5][0]       # 第四日
            result6 = i[6][0]       # 第五日

            if result1 and result2:
                kp0, zg0, zd0, sp0 = result0.kp, result0.zg, result0.zd, result0.sp
                kp1, zg1, zd1, sp1 = result1.kp, result1.zg, result1.zd, result1.sp
                kp2, zg2, zd2, sp2 = result2.kp, result2.zg, result2.zd, result2.sp
                kp3, zg3, zd3, sp3 = result3.kp, result3.zg, result3.zd, result3.sp
                kp4, zg4, zd4, sp4 = result4.kp, result4.zg, result4.zd, result4.sp
                kp5, zg5, zd5, sp5 = result5.kp, result5.zg, result5.zd, result5.sp
                kp6, zg6, zd6, sp6 = result6.kp, result6.zg, result6.zd, result6.sp
                # 次日开盘处于当天收盘 次日最高除以当天收盘, 次日最低除以当天收盘,次日收盘除以当天收盘

                kp2_sp0 = round(sp2/sp0, 5)
                print(sp2,kp0,sp2/sp0)

                kp2_sp1 = round(kp2/sp1, 5)
                zg2_sp1 = round(zg2/sp1, 5)
                zd2_sp1 = round(zd2/sp1, 5)
                sp2_sp1 = round(sp2/sp1, 5)

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


                # 次日sp/昨日收盘

                date1 = do_the_date(result1, kp2_sp1, zg2_sp1, zd2_sp1, sp2_sp1, kp3_sp1, zg3_sp1, zd3_sp1, sp3_sp1,
                                    kp4_sp1, zg4_sp1, zd4_sp1, sp4_sp1, kp5_sp1, zg5_sp1, zd5_sp1, sp5_sp1
                                    , kp6_sp1, zg6_sp1, zd6_sp1, sp6_sp1, kp2_sp0)

                show_result_list.append(date1)
        b = time.time()
        # print(b)
        print(b-a)
        return render(request, "search_boll.html", {"show_result_list": show_result_list})

    return HttpResponse('没有')



def do_the_date(result1, kp2_sp1, zg2_sp1, zd2_sp1, sp2_sp1, kp3_sp1, zg3_sp1, zd3_sp1, sp3_sp1, kp4_sp1, zg4_sp1,
                zd4_sp1, sp4_sp1, kp5_sp1, zg5_sp1, zd5_sp1, sp5_sp1, kp6_sp1, zg6_sp1, zd6_sp1, sp6_sp1,kp2_sp0):
    date = [result1.code, result1.date, result1.name, kp2_sp1, zg2_sp1, zd2_sp1, sp2_sp1, kp3_sp1, zg3_sp1, zd3_sp1,
            sp3_sp1, kp4_sp1, zg4_sp1, zd4_sp1, sp4_sp1, kp5_sp1, zg5_sp1, zd5_sp1, sp5_sp1, kp6_sp1, zg6_sp1,
            zd6_sp1, sp6_sp1,kp2_sp0]
    return date


def compute_final_result(r2):

    result_li = []  # 计算结果存储列表

    three0_days = []  # 31天数据存储列表

    flag_day = 0  			# 天数标杆
    for i in r2:

        # count_time, '/', len(r2)# 可标记#############################################################3

        flag_day += 1		# 因为需要大前天的数据所以从第4天开始算起
        # print(i[0].date)
        # print('111111111')
        if len(three0_days) != 0:
            # print('222222222')
            if i[0].code == three0_days[-1][0].code:  # 如果r2表中的股票代码等于30天列表的的代码
                # print('333333333')
                three0_days.append(i)     # 将前31天数据加入列表

                if flag_day == 35:
                    # print(i[0].date)
                    # print('444444')
                    result0, result1, result2, result3, result4,result5,result6 = compute_after_20_result(three0_days)
                    # print(result1, result2, result3)
                    # print(result1, result2)
                    if result1: 						# 如果存在查找结果
                        # print('55555555')
                        result_li.append((result0, result1, result2, result3, result4,result5,result6))    # 将查找结果加入到结果列表

                elif flag_day > 35:
                    # print('66666666')
                    three0_days.pop(0)  # 删除第一天的值是列表保持4天的数据值

                    result0, result1, result2, result3, result4,result5,result6 = compute_after_20_result(three0_days)
                    # print(result1, result2,result3)
                    if result1: 						# 如果存在查找结果
                        # print('7777777')
                        result_li.append((result0, result1, result2,result3,result4,result5,result6)) 	# 将查找结果加入到结果列表

            elif i[0].code != three0_days[-1][0].code:   # 如果r2表中的股票代码不等于30天列表的的代码
                # print('88888888')
                three0_days = []
                flag_day = 0
        elif len(three0_days) == 0:
            # print('99999999')
            three0_days.append(i)
    # print(result_li)
    return result_li


def compute_after_20_result(four_days):
    """根据传入对象的结果计算要求值
    four_days的格式为:
    [大前天,上,中,下),(前天,上,中,下),(昨天obj,上,中,下),(当天obj,上,中,下)]
    """
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

    if four_days[-6][0].sp/four_days[-7][0].sp>1.5:  # 老规矩能改的地方 只不过是今天变成了[-6]








        return four_days[-7],four_days[-6], four_days[-5], four_days[-4],four_days[-3],four_days[-2],four_days[-1] # 别碰这一行

    else:

        return 0, 0, 0, 0, 0, 0,0








def compute_boll(r1):
    """计算布林线
    MA20 = 20天内收盘价之和/20
    MD = sqrt(sum((当天收盘价-MA20)**2+...)/19)
    MB(中间的线) = MA20
    UP(上边的线) = MB + 2*MD
    ND(下面的先) = MB-2*MD
    """

    r2 = []      # 展示结果的列表
    ma20_list = []      # 创建ma存储列表
    r2_sp = [] 	# 相同股票收盘价格列表
    r2_md = []  # 相同股票计算md参照列表
    flag = []    # 标杆列表
    f = 0        # 标杆f

    for i in r1:    # 循环股票
        if f == 0:  # 确认标杆f是否为0
            f = 1   # 如果为零 使标杆=1
            flag.append(i)  # 将被比较对象加入flag列表中

            r2_sp.append(i.sp)  # 将第一次循环的的对象收盘价放入相同股票的列表中

        else: 				# 如果flag不为空

            if i.code != flag[0].code:   # 如果被比较对象不等于当前循环对象
                flag.clear() 		# 清空被比较对象列表
                r2_sp.clear()  # 清空相同股票的每日对象
                r2_md.clear()  # 将md列表清空
                ma20_list.clear()   # 将 ma_list列表清空
                f = 0				# 将标杆f设置成0
            else: 					# 如果被比较对象code大呢关于当前循环对象code

                r2_sp.append(i.sp)  # 将从第二次循环的收盘价放入收盘价列表中

                if len(r2_sp) >= 20:  # 如果加入列表的收盘价个数大于等于20个

                    ma20, new_r2_sp = make_20ma(r2_sp)  # 执行计算20MA
                    ma20_z, new_r2_sp_z = make_20ma_z(r2_sp)

                    if new_r2_sp != 0: 		# 如果返回的新列表不为零

                        r2_sp = new_r2_sp 	# 是收盘列表等于新列表

                    ma20_list.append(ma20)  # 将ma20加入到 ma20列表中

                    md = make_md(r2_sp, ma20)    # 计算md
                    md_z = make_md_z(r2_sp, ma20_z)

                    mb = ma20  					# 计算mb

                    up = mb + 2*md 				# 计算up

                    nd = mb - 2*md 				# 计算nd

                    mb_z = ma20_z

                    up_z =  mb_z + 2*md_z
                    nd_z =  mb_z - 2*md_z

                    # print('4444444444444444', up, nd)
                    r2.append((i, up, mb, nd,up_z,mb_z,nd_z))

                flag[0] = i   # 被比较对象等于当前循环对象

    return r2


def make_md(r2_sp, ma20):
    """计算 MD
    MD = sqrt(sum((当天收盘价-MA20)**2+...)/19)
    """
    import math
    from decimal import Decimal
    from copy import deepcopy

    r2_sp_test = deepcopy(r2_sp)
    r2_sp_test[-1] = r2_sp_test[-2] * Decimal.from_float(1.1)
    # print('1111111111111', ma20)
    # print('22222222222222', r2_sp_test)

    sp_ma20_list = []   	# 将(每日收盘-ma2)**2 的列表

    for sp in r2_sp_test: 		# 对20日收盘价循环

        sp_ma20_list.append((sp-ma20)**2)  # 将 (每日收盘-ma2)**2 加入到列表

    md = math.sqrt(sum(sp_ma20_list)/19)    # 求md
    # print('33333333333333333333333',md)

    return Decimal.from_float(md)


def make_20ma(r2_sp):
    """计算20ma
    MA20 = 20天内收盘价之和/20
    """
    from copy import deepcopy
    from decimal import Decimal

    r2_sp_test = deepcopy(r2_sp)
    r3_sp_test = deepcopy(r2_sp)
    r2_sp_test[-1] = r2_sp_test[-2]*Decimal.from_float(1.1)



    if len(r2_sp_test) == 20:        # 如果收盘列表达到20天长度

        # print(r2_sp_test[-1],r2_sp_test[-2],r2_sp_test[-3],r2_sp_test[-4],r2_sp_test[-5],r2_sp_test[-6],r2_sp_test[-7],
        #       r2_sp_test[-8],r2_sp_test[-9],r2_sp_test[-10],r2_sp_test[-11],r2_sp_test[-12],r2_sp_test[-13],r2_sp_test[-14],
        #     r2_sp_test[-15],r2_sp_test[-16],r2_sp_test[-17],r2_sp_test[-18],r2_sp_test[-19],r2_sp_test[-20])

        ma20 = sum(r2_sp_test)/20	    # 计算ma20
        # print(ma20)
        return ma20, 0			# 返回ma20 和0

    elif len(r2_sp_test) > 20: 		# 如果收盘列表天数 大于20

        r2_sp_test.pop(0)			# 除去列表头部的天数

        ma20 = sum(r2_sp_test)/20 	# 计算ma20

        r2_sp.pop(0)

        return ma20, r2_sp       # 返回ma20 和 除去头部天数的新列表




def index(request):

    return HttpResponse("hello")







































def make_md_z(r2_sp, ma20):
    """计算 MD
    MD = sqrt(sum((当天收盘价-MA20)**2+...)/19)
    """
    import math
    from decimal import Decimal

    sp_ma20_list_z = []   	# 将(每日收盘-ma2)**2 的列表

    for sp in r2_sp: 		# 对20日收盘价循环

        sp_ma20_list_z.append((sp-ma20)**2)  # 将 (每日收盘-ma2)**2 加入到列表

    md_z = math.sqrt(sum(sp_ma20_list_z)/19)    # 求md

    return Decimal.from_float(md_z)


def make_20ma_z(r2_sp):
    """计算20ma
    MA20 = 20天内收盘价之和/20
    """

    if len(r2_sp) == 20:        # 如果收盘列表达到20天长度

        ma20 = sum(r2_sp)/20	    # 计算ma20

        return ma20, 0			# 返回ma20 和0

    elif len(r2_sp) > 20: 		# 如果收盘列表天数 大于20

        r2_sp.pop(0)			# 除去列表头部的天数

        ma20_z = sum(r2_sp)/20 	# 计算ma20

        return ma20_z, r2_sp       # 返回ma20 和 除去头部天数的新列表

