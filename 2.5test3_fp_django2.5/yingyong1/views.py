import os
import decimal
import math
import copy
import json
from django.shortcuts import HttpResponse, render
from redis import *





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
        for file in self.file_list:     # 循环目录文件
            print(file)
            self.one_file_data = None
            data_all_list = []          # 创建批量加入数据库的列表
            sp_20_list = []
            lines_list = self.read_file_lines(file)
            self.code, self.name = self.take_code_name(lines_list)
            # code_list.append(code)

            for info in lines_list[1:]:
                return_value = self.take_date_kp_zg_zd_cjl_cje(info)

                if return_value != None:
                    self.date, self.kp, self.zg, self.zd, self.sp, cjl, cje = self.take_date_kp_zg_zd_cjl_cje(info)
                    sp_20_list.append(decimal.Decimal(self.sp))

                    if len(sp_20_list) >= 20:
                        self.today_ma20, self.today_md, self.today_bls, self.today_blz, self.today_blx, self.today_ma2011,\
                        self.today_md11, self.today_bls11,self.today_blz11,\
                        self.today_blx11 = self.take_ma20_md_bollup_bollcenter_bolldown(sp_20_list)
                        make_obj = MakeObj(self.code, self.name, self.date, float(self.kp), float(self.zg),
                                           float(self.zd), float(self.sp), self.today_ma20, self.today_md,
                                           self.today_bls, self.today_blz, self.today_blx, self.today_ma2011,
                                           self.today_md11,self.today_bls11,self.today_blz11,self.today_blx11)
                        make_obj_dict = make_obj.__dict__

                        all_list.append(make_obj_dict)
                    else:
                        make_obj = MakeObj(self.code, self.name, self.date, self.kp, self.zg,
                                            self.zd, self.sp)
                        make_obj_dict = make_obj.__dict__
                        all_list.append(make_obj_dict)



        redis_obj = UseRedis()
        redis_obj.put_data_in_redis(all_list)


    def write_data_all_list_to_result(self, date_all_list, file_name):
        with open(os.getcwd()+'\\result\\'+ file_name, 'w', encoding="GBK")as f:
            for line in date_all_list:
                f.write(str(line)+'\n')



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



class MakeObj:

    def __init__(self, code, name, date, kp, zg, zd, sp, today20=0, today_md=0,
                 today_bls=0, today_blz=0, today_blx=0, today_ma2011=0, today_md11=0,
                 today_bls11=0, today_blz11=0, today_blx11=0):
        self.code = code
        self.name = name
        self.date = date
        self.kp = kp
        self.zg = zg
        self.zd = zd
        self.sp = sp
        self.today20 = today20
        self.today_md = today_md
        self.today_bls = today_bls
        self.today_blz = today_blz
        self.today_blx = today_blx
        self.today_ma2011 = today_ma2011
        self.today_md11 = today_md11
        self.today_bls11 = today_bls11
        self.today_blz11 = today_blz11
        self.today_blx11 = today_blx11


class TakeFilePlace:

    def __init__(self):
        self.work_list_path = os.getcwd()+'\\export\\'
        self.work_list_filename_list = os.listdir(self.work_list_path)



class ClearData:

    def __init__(self):
        self.result_list = []
        self.days_30_obj_list = []
        self.today_flag = 0
        self.data_one_obj_list = []
        self.all_list = []


    def computed_result(self):

        if self.data_one_obj_list[-1]['sp']/self.data_one_obj_list[-2]['sp']>100:
            self.result_list.append(self.data_one_obj_list[-1])


class UseRedis:

    def __init__(self):
        self.sr = StrictRedis()

    def put_data_in_redis(self, data):
        json_data = json.dumps(data)

        self.sr.set('haha', json_data)
        # self.take_data_from_redis(file_name)

    def take_one_data_from_redis(self):
        one_data = json.loads(self.sr.get('haha'))
        return one_data

    def del_data(self):
        self.sr.flushdb()



def main2():
    use_redis = UseRedis()
    all_data = use_redis.take_one_data_from_redis()
    result = compute_final_result(all_data)
    # [({0}, {1}, {2}, {3}, {4},{5}), ({0}, {1}, {2}, {3}, {4}), ({0}, {1}, {2}, {3}, {4}), ({0}, {1}, {2}, {3}, {4}),({0}, {1}, {2}, {3}, {4})]
    write_to_file_result_list = []
    if result != []:
        for five_day_obj in result:

            result0 = five_day_obj[0]  # 昨日
            result1 = five_day_obj[1]  # 当天
            result2 = five_day_obj[2]  # 第一日
            result3 = five_day_obj[3]  # 第二日
            result4 = five_day_obj[4]  # 第三日
            result5 = five_day_obj[5]  # 第四日
            result6 = five_day_obj[6]  # 第五日

            kp0, zg0, zd0, sp0 = result0['kp'], result0['zg'], result0['zd'], result0['sp']
            kp1, zg1, zd1, sp1 = result1['kp'], result1['zg'], result1['zd'], result1['sp']
            kp2, zg2, zd2, sp2 = result2['kp'], result2['zg'], result2['zd'], result2['sp']
            kp3, zg3, zd3, sp3 = result3['kp'], result3['zg'], result3['zd'], result3['sp']
            kp4, zg4, zd4, sp4 = result4['kp'], result4['zg'], result4['zd'], result4['sp']
            kp5, zg5, zd5, sp5 = result5['kp'], result5['zg'], result5['zd'], result5['sp']
            kp6, zg6, zd6, sp6 = result6['kp'], result6['zg'], result6['zd'], result6['sp']

            kp2_sp0 = round(sp2 / sp0, 5)


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
            write_to_file_result_list.append([result1['code'], result1['name'], result1['date'], kp2_sp0, kp2_sp1,
                                              zg2_sp1, zd2_sp1, sp2_sp1, kp3_sp1, zg3_sp1, zd3_sp1, sp3_sp1, kp4_sp1,
                                              zg4_sp1, zd4_sp1, sp4_sp1, kp5_sp1, zg5_sp1, zd5_sp1, sp5_sp1, kp6_sp1,
                                              zg6_sp1, zd6_sp1, sp6_sp1])

        return write_to_file_result_list


def compute_final_result(r2):

    result_li = []  # 计算结果存储列表

    three0_days = []  # 31天数据存储列表

    flag_day = 0  # 天数标杆
    for i in r2:
        # print(i)

        # count_time, '/', len(r2)# 可标记#############################################################3

        flag_day += 1  # 因为需要大前天的数据所以从第4天开始算起

        if len(three0_days) != 0:

            if i['code'] == three0_days[-1]['code']:  # 如果r2表中的股票代码等于30天列表的的代码

                three0_days.append(i)  # 将前31天数据加入列表

                if flag_day == 35:

                    result0, result1, result2, result3, result4, result5, result6 = compute_after_20_result(
                        three0_days)

                    if result1:  # 如果存在查找结果

                        result_li.append(
                            (result0, result1, result2, result3, result4, result5, result6))  # 将查找结果加入到结果列表

                elif flag_day > 35:

                    three0_days.pop(0)  # 删除第一天的值是列表保持4天的数据值

                    result0, result1, result2, result3, result4, result5, result6 = compute_after_20_result(
                        three0_days)

                    if result1:  # 如果存在查找结果
                        # print('7777777')
                        result_li.append(
                            (result0, result1, result2, result3, result4, result5, result6))  # 将查找结果加入到结果列表

            elif i['code'] != three0_days[-1]['code']:  # 如果r2表中的股票代码不等于30天列表的的代码

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
    # ['kp']      ['zg']      ['zd']      ['sp']
    # ['today20']         ['today_md']        ['today_bls']       ['today_blz']       ['today_blx']
    # ['today_ma2011']    ['today_md11']      ['today_bls11']     ['today_blz11']     ['today_blx11']

    if four_days[-8]['bls'] / four_days[-9]['bls'] > 1.04 and \
            four_days[-6]['zd'] / four_days[-7]['sp'] > 0.91 and \
            four_days[-6]['sp'] / four_days[-7]['sp'] < 0.98 and \
            four_days[-6]['sp'] / four_days[-6]['blz'] < 1.07 and \
            four_days[-6]['blz'] / four_days[-7]['blz'] > 1.01 and \
            four_days[-6]['bls'] / four_days[-6]['blz'] < 1.25 and \
            (four_days[-6]['blz'] / four_days[-7]['blz'] - 1) * 10 - (
            four_days[-6]['sp'] / four_days[-6]['blz']) > -1 and \
            (four_days[-7]['blz'] / four_days[-8]['blz'] - 1) * 10 - (four_days[-7]['sp'] / four_days[-7]['blz']) < -1:


        return four_days[-7], four_days[-6], four_days[-5], four_days[-4], four_days[-3], four_days[-2], four_days[
            -1]  # 别碰这一行

    else:

        return 0, 0, 0, 0, 0, 0, 0

def main1():
    a = Dofile()
    a.take_data()

def main3():
    u = UseRedis()
    u.del_data()

def insert_data1(request):
    main1()
    return HttpResponse('哈哈')

def search_boll(request):
    result = main2()
    if result != None:
        return render(request, 'search_boll.html', {'result': result})
    else:
        return HttpResponse('没有')


def del_database(request):
    main3()
    return HttpResponse('数据库删除完毕！！！')

