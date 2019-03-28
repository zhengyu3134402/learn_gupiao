import os
import decimal
import math
import re
import datetime
import copy
import json





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


            # print(self.one_file_data)
        redis_obj = UseRedis()
        redis_obj.put_data_in_redis(all_list)
            # self.write_data_all_list_to_result(data_all_list, file)

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

    def save_putindatabase_objcode(self, code_list):
        '''把插入到数据库中的对象code写入到obj_code.txt中'''

        with open(os.getcwd()+'\\test111\\obj_code.txt', 'w')as f:
            for obj_code in code_list:
                f.write(obj_code+'\n')


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


from redis import *
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


def main():
    a = Dofile()
    a.take_data()

if __name__ == '__main__':
    main()






#
# def put_database(request):
#     """插入数据页面的处理"""
#     obj = Dofile()
#     args_command = request.GET.get('ARGS', '0')
#     if request.method == "POST":
#         files = request.FILES.getlist('files')
#         for file in files:
#             with open(obj.workfile_position + '\\' + file.name, 'wb+') as f:
#                 for i in file:
#                     f.write(i)
#
#     elif args_command == "delete_database":
#         cursor = connection.cursor()
#         cursor.execute("truncate table yingyong1_gupiao")
#         obj = Dofile()
#         obj.delete_file()
#         return HttpResponse(json.dumps({'ok': '200'}))
#
#     elif args_command == "put_in_database":
#         obj.take_data()
#
#     elif args_command == "progress_pro":
#         return HttpResponse(json.dumps({'ok': file_numbers,'file_nums': file_lens}))
#
#     return render(request, 'put_database.html')
#
#
# def start_search(request):
#     """搜索结果页面的处理"""
#     if request.method == 'POST':
#
#         start_date = request.POST.get('start_date')
#         end_date = request.POST.get('end_date')
#         text_code = request.POST.get('textarea')
#
#         a = Analyse_data(start_date, end_date, text_code)
#         result = a.take_result() # [(今日对象，次日对象),.....]
#
#         rep1 = render(request, 'start_search.html', {'result': result})
#         rep2 = render(request, 'start_search.html')
#         rep1.set_cookie('start_date', start_date, expires=99999)
#         rep1.set_cookie('end_date', end_date, expires=99999)
#         rep1.set_cookie('textarea', text_code, expires=99999)
#
#         if result != []:
#             return rep1
#         return rep2
#
#     return HttpResponse('haha')
#
#
# def search(request):
#     """搜索页面的处理"""
#     if request.COOKIES.get('start_date') and request.COOKIES.get('end_date') and request.COOKIES.get('textarea'):
#         start_date = request.COOKIES.get('start_date')
#         end_date = request.COOKIES.get('end_date')
#         text_code = request.COOKIES.get('textarea')
#         return render(request, 'search.html', {'start_date_cookies':start_date, 'end_date_cookies': end_date,
#                                                'textarea_cookies':text_code, 'num':1})
#     return render(request, 'search.html', {'num': 0})
#
#
# def system(request):
#     """系统页面的处理"""
#     return render(request, 'system.html')
#
#
# def index(request):
#     """主页的处理"""
#     return render(request, 'index.html')
#
#
#
#
