

import pymysql
from pymysql.err import InternalError
conn = pymysql.connect(host='127.0.0.1', port=3306, user='zhengyu', passwd='3134402', db='test3')

cursor = conn.cursor()

try:
    cursor.execute("drop table gupiao") # 执行原生sql语句
except InternalError:
    cursor.close()

    conn.close()
    print('======================================================')
    print('！！！！！！！！数据删除完毕！！！！！！！！！！！！！')
    print('======================================================')
else:
    cursor.close()

    conn.close()

    print('======================================================')
    print('！！！！！！！！数据删除完毕！！！！！！！！！！！！！')
    print('======================================================')

