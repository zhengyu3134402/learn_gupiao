import os
import decimal
import math
import re
import datetime
import copy
import json
from django.shortcuts import render, HttpResponse
from yingyong1.models import Gupiao
from django.db.utils import IntegrityError
from django.db import connection

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# 代码重构

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 全局变量
file_numbers = 0
file_lens = 0
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


class Dofile:     # 创建处理文件类

    def __init__(self):         # 初始化类
        self.workfile_position = os.getcwd() + '\\yingyong1\export'  # 初始化执行文件目录位置
        self.file_list = self.get_update_filelist()     # 初始化执行文件列表
        self.count_file_flag = 0   # 初始化计数操作标杆为空列表
        self.file_num = len(self.file_list)  # 初始化处理文件的个数

    def get_update_filelist(self):
        """获取上传目录文件列表"""
        file_list = os.listdir(self.workfile_position)
        return file_list

    def delete_file(self):
        '''删除export目录中的所有文件'''
        for i in self.file_list:
            os.remove(self.workfile_position+'\\'+i)

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
        for file in self.file_list:     # 循环目录文件
            print(file)

            global file_numbers
            file_numbers += 1

            global file_lens
            file_lens = len(self.file_list)

            data_all_list = []          # 创建批量加入数据库的列表
            sp_20_list = []
            lines_list = self.read_file_lines(file)
            code, name = self.take_code_name(lines_list)
            code_list.append(code)

            for info in lines_list[1:]:
                return_value = self.take_date_kp_zg_zd_cjl_cje(info)

                if return_value != None:
                    date, kp, zg, zd, sp, cjl, cje = self.take_date_kp_zg_zd_cjl_cje(info)
                    sp_20_list.append(decimal.Decimal(sp))

                    if len(sp_20_list) >= 20:
                        today_ma20, today_md, today_bollup, today_bollcenter, today_bolldown, today_ma20_1_1, today_md_1_1,\
    today_bollup_1_1,today_bollcenter_1_1, today_bolldown_1_1 = self.take_ma20_md_bollup_bollcenter_bolldown(sp_20_list)
                        data_all_list.append(Gupiao(code=code, name=name, date=date, kp=kp, zg=zg,
                                                    zd=zd, sp=sp, cjl=cjl, cje=cje, today_ma20=today_ma20,
                                                    today_md=today_md, bls=today_bollup,
                                                    blz=today_bollcenter, blx=today_bolldown,today_ma20_1_1=today_ma20_1_1,
                                                    today_md_1_1=today_md_1_1, bls_1_1=today_bollup_1_1,
                                                    blz_1_1=today_bollcenter_1_1, blx_1_1=today_bolldown_1_1))
                    else:
                        # 将以上得出的内容最为Gupiao模型的参数，构成一个对象加入到列表中
                        data_all_list.append(Gupiao(code=code, name=name, date=date, kp=kp, zg=zg,
                                            zd=zd, sp=sp, cjl=cjl, cje=cje))

            try:  # 补获已经存在的数据
                Gupiao.objects.bulk_create(data_all_list)   # 将对象列表批量加入到数据库中
            except IntegrityError:     # 若数据已经在数据库中则打印下调提示信息
                print("此数据已经存在，不在插入")
        self.save_putindatabase_objcode(code_list)
        file_numbers = 0
        file_lens = 0
        self.delete_file()

    def take_ma20_md_bollup_bollcenter_bolldown(self, sp_20_list):
        '''根据数据计算出ma20和布林线'''
        new_sp_20_list = self.makesure_sp_list_20(sp_20_list)
        compute_boll = Compute_boll(new_sp_20_list)
        today_ma20 = compute_boll.today_ma20
        today_md = compute_boll.today_md
        today_bollup = compute_boll.bls
        today_bollcenter = compute_boll.blz
        today_bolldown = compute_boll.blx
        today_ma20_1_1 = compute_boll.today_ma20_1_1
        today_md_1_1 = compute_boll.today_md_1_1
        today_bollup_1_1 = compute_boll.bls_1_1
        today_bollcenter_1_1 = compute_boll.blz_1_1
        today_bolldown_1_1 = compute_boll.blx_1_1

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


class Analyse_data:   # 分析数据模块

    def __init__(self , start_date, end_date, text_code):
        self.start_date = start_date
        self.end_date = end_date
        self.text_code = text_code
        self.code = None
        self.target_filename = self.take_target_filename()
        self.clear_text_code = self.clear_text_code()
        self.for_each_gupiao = None
        self.clear_start_date = self.clear_start_date_function()
        self.clear_end_date = self.clear_end_date_function()
        self.clear_start_date_id = None
        self.clear_end_date_id = None
        # _______
        self.stop = 0
        #------------

    def take_target_filename(self):
        '''获取已经在数据库中的对象code'''
        with open(os.getcwd()+'\\test111\\obj_code.txt', 'r')as f:
            code_list = f.readlines()  # ['600000\n', '600004\n', '600006\n', '600007\n', '600008\n', '600009\n', '600010\n']
            return code_list

    def clear_text_code(self):
        '''获取浏览器中用户输入的公式并进行转换'''
        new_text_code1 = self.text_code.strip()
        new_text_code2 = re.sub(r'([a-zA-z|_1]+)(\[0\])', r'today_gupiao.\1', new_text_code1) # 将带有[0] 替换成today_gupiao.xx
        new_text_code3 = re.sub(r'([a-zA-z]+)\[(-\d+)\]', r'for_each_gupiao_list[index_flag\2].\1', new_text_code2) #将带有[-xx]部分替换正操作变量
        new_text_code4 = re.sub(r'([a-zA-z]+)\[(\+\d+)\]', r'for_each_gupiao_list[index_flag\2].\1',new_text_code3) # 处理[+1]
        new_text_code5 = re.sub(r'\r\n', r' and ', new_text_code4)
        print(new_text_code5)

        return new_text_code5

    def take_result(self):
        '''根据转换后的用户公式进行计算数据'''
        all_result = []
        flag_mark = 0
        for code in self.target_filename:
            self.stop = 0
            flag_mark += 1
            print(str(flag_mark)+'/'+str(len(self.target_filename)))

            self.code = code
            self.for_each_gupiao = self.with_code_take_gupiaoobj()
            self.clear_start_date = self.clear_start_date_function()
            self.clear_end_date = self.clear_end_date_function()
            # -----------------
            if self.stop == 1:
                continue
            # -----------------
            self.clear_start_date_id, self.clear_end_date_id = self.with_new_start_date_end_date_take_id()

            new_for_each_gupiao = self.with_new_date_get_for_each_gupiao()


            result = self.with_condition_computed_result(new_for_each_gupiao)
            if result != []:
                all_result.append(result)
        return all_result


    def with_condition_computed_result(self, new_for_each_gupiao):
        """根据客户的书写的条件计算结果"""
        result = []

        for_each_gupiao_list = list(new_for_each_gupiao)  # 将QuerySet类型转换成list类型，支持负索引操作
        max_database_num = self.take_max_database_num()
        index_flag = 0



        for today_gupiao in for_each_gupiao_list:
            if index_flag >= max_database_num:
                if eval(self.clear_text_code):
                    days_5_obj_list = self.take_5_days_from_self_for_each_gupiao()
                    for_each_gupiao_list = self.take_5_days_to_for_each_gupiao_list(for_each_gupiao_list, days_5_obj_list)

                    result_5_days_computed = self.take_5days_kp_zg_zd_sp_computed(today_gupiao, for_each_gupiao_list, index_flag)


                    result.append((today_gupiao, result_5_days_computed))
            index_flag += 1

        return result

    def take_next_5day_kp_zg_zd_sp_computed(self, today_gupiao, for_each_gupiao_list, index_flag, day_num):

        kp_next_sp_today = round(for_each_gupiao_list[index_flag + day_num].kp / today_gupiao.sp, 5)
        zg_next_sp_today = round(for_each_gupiao_list[index_flag + day_num].zg / today_gupiao.sp, 5)
        zd_next_sp_today = round(for_each_gupiao_list[index_flag + day_num].zd / today_gupiao.sp, 5)
        sp_next_sp_today = round(for_each_gupiao_list[index_flag + day_num].sp / today_gupiao.sp, 5)

        return [kp_next_sp_today, zg_next_sp_today, zd_next_sp_today, sp_next_sp_today]

    def take_5days_kp_zg_zd_sp_computed(self, today_gupiao, for_each_gupiao_list, index_flag):

        next1_day_list = self.take_next_5day_kp_zg_zd_sp_computed(today_gupiao, for_each_gupiao_list, index_flag, 1)
        next2_day_list = self.take_next_5day_kp_zg_zd_sp_computed(today_gupiao, for_each_gupiao_list, index_flag, 2)
        next3_day_list = self.take_next_5day_kp_zg_zd_sp_computed(today_gupiao, for_each_gupiao_list, index_flag, 3)
        next4_day_list = self.take_next_5day_kp_zg_zd_sp_computed(today_gupiao, for_each_gupiao_list, index_flag, 4)
        next5_day_list = self.take_next_5day_kp_zg_zd_sp_computed(today_gupiao, for_each_gupiao_list, index_flag, 5)

        return [next1_day_list, next2_day_list, next3_day_list, next4_day_list, next5_day_list]



    def take_5_days_to_for_each_gupiao_list(self,for_each_gupiao_list, days_5_obj_list):
        for one_day_list in days_5_obj_list:
            for_each_gupiao_list = for_each_gupiao_list + one_day_list
        return for_each_gupiao_list



    def take_5_days_from_self_for_each_gupiao(self):

        next1_day = list(self.for_each_gupiao.filter(id=self.clear_end_date_id + 1))
        next2_day = list(self.for_each_gupiao.filter(id=self.clear_end_date_id + 2))
        next3_day = list(self.for_each_gupiao.filter(id=self.clear_end_date_id + 3))
        next4_day = list(self.for_each_gupiao.filter(id=self.clear_end_date_id + 4))
        next5_day = list(self.for_each_gupiao.filter(id=self.clear_end_date_id + 5))

        return [next1_day, next2_day, next3_day, next4_day, next5_day]

    def with_new_date_get_for_each_gupiao(self):
        """根据客户选的日期对对象进行日期赛选"""

        for_each_gupiao_list = self.for_each_gupiao.filter(id__range=[self.clear_start_date_id-self.take_max_database_num(), self.clear_end_date_id])
        return for_each_gupiao_list

    def take_max_database_num(self):
        """根据客户的需求最大天数扩大数据的天数范围"""
        new_range_num = []
        new_text_code1 = self.text_code.strip()
        range_num = re.findall(r'\[(-\d+|\d+)\]', new_text_code1)
        # print(range_num)
        for str_num in range_num:
            new_range_num.append(int(str_num))
        return abs(min(new_range_num))

    def with_code_take_gupiaoobj(self):

        return Gupiao.objects.filter(code=int(self.code.strip()))

    def with_new_start_date_end_date_take_id(self):
        clear_start_date_obj = self.for_each_gupiao.filter(date=self.do_self_start_date_mysql(self.clear_start_date))
        clear_end_date_obj = self.for_each_gupiao.filter(date=self.do_self_end_date_mysql(self.clear_end_date))
        return clear_start_date_obj[0].id, clear_end_date_obj[0].id






    def clear_start_date_function(self):
        """对客户的选择的开始日期进行确定，如果所选日期不存在，向前获取日期"""
        if self.for_each_gupiao == None:
            return None
        else:
            flag_num = 0
            # --------
            flag_num1 = 0
            # ----------
            self_start_date_copy = copy.deepcopy(self.start_date)

            while not self.for_each_gupiao.filter(date=self.do_self_start_date_mysql(self_start_date_copy)):

                if flag_num >= 5:
                    # --------
                    flag_num1 +=1
                    if flag_num1 >=5:
                        self.stop = 1
                        break
                    # -------
                    new_start_date1 = datetime.datetime.strptime(self_start_date_copy, '%Y-%m-%d')
                    one_day = datetime.timedelta(days=1)
                    new_start_date2 = new_start_date1 + one_day
                    self_start_date_copy = datetime.datetime.strftime(new_start_date2, '%Y-%m-%d')
                    continue





                new_start_date1 = datetime.datetime.strptime(self_start_date_copy, '%Y-%m-%d')
                one_day = datetime.timedelta(days=1)
                new_start_date2 = new_start_date1-one_day
                self_start_date_copy = datetime.datetime.strftime(new_start_date2, '%Y-%m-%d')
                flag_num +=1

            return self_start_date_copy

    def do_self_start_date_mysql(self, self_start_date_copy):
        """将开始日期转换成数据库接收的类型"""

        return re.sub(r'\-', r'/', self_start_date_copy)


    def clear_end_date_function(self):
        """对客户的选择的结束日期进行确定，如果所选日期不存在，向后获取日期"""
        if self.for_each_gupiao == None:

            return None
        else:
            self_end_date_copy = copy.deepcopy(self.end_date)
            flag = 0
            while not self.for_each_gupiao.filter(date=self.do_self_end_date_mysql(self_end_date_copy)):
                new_end_date1 = datetime.datetime.strptime(self_end_date_copy, '%Y-%m-%d')
                one_day = datetime.timedelta(days=1)
                new_end_date2 = new_end_date1+one_day
                self_end_date_copy = datetime.datetime.strftime(new_end_date2, '%Y-%m-%d')
                flag += 1
                # --------
                if flag == 5:
                    self.stop = 1
                    break
                # --------
            return self_end_date_copy

    def do_self_end_date_mysql(self, self_end_date_copy):
        """将结束日期转换成数据库接收的类型"""
        return re.sub(r'\-', r'/', self_end_date_copy)









def put_database(request):
    """插入数据页面的处理"""
    obj = Dofile()
    args_command = request.GET.get('ARGS', '0')
    if request.method == "POST":
        files = request.FILES.getlist('files')
        for file in files:
            with open(obj.workfile_position + '\\' + file.name, 'wb+') as f:
                for i in file:
                    f.write(i)

    elif args_command == "delete_database":
        cursor = connection.cursor()
        cursor.execute("truncate table yingyong1_gupiao")
        obj = Dofile()
        obj.delete_file()
        return HttpResponse(json.dumps({'ok': '200'}))

    elif args_command == "put_in_database":
        obj.take_data()

    elif args_command == "progress_pro":
        return HttpResponse(json.dumps({'ok': file_numbers,'file_nums': file_lens}))

    return render(request, 'put_database.html')


def start_search(request):
    """搜索结果页面的处理"""
    if request.method == 'POST':

        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        text_code = request.POST.get('textarea')

        a = Analyse_data(start_date, end_date, text_code)
        result = a.take_result() # [(今日对象，次日对象),.....]

        rep1 = render(request, 'start_search.html', {'result': result})
        rep2 = render(request, 'start_search.html')
        rep1.set_cookie('start_date', start_date, expires=99999)
        rep1.set_cookie('end_date', end_date, expires=99999)
        rep1.set_cookie('textarea', text_code, expires=99999)

        if result != []:
            return rep1
        return rep2

    return HttpResponse('haha')


def search(request):
    """搜索页面的处理"""
    if request.COOKIES.get('start_date') and request.COOKIES.get('end_date') and request.COOKIES.get('textarea'):
        start_date = request.COOKIES.get('start_date')
        end_date = request.COOKIES.get('end_date')
        text_code = request.COOKIES.get('textarea')
        return render(request, 'search.html', {'start_date_cookies':start_date, 'end_date_cookies': end_date,
                                               'textarea_cookies':text_code, 'num':1})
    return render(request, 'search.html', {'num': 0})


def system(request):
    """系统页面的处理"""
    return render(request, 'system.html')


def index(request):
    """主页的处理"""
    return render(request, 'index.html')




