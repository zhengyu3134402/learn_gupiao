

import pymysql
from pymysql.err import InternalError
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='a3134402', db='testai3')

cursor = conn.cursor()

try:
    cursor.execute("drop table gupiao_info")  # 执行原生sql语句
except InternalError:
    cursor.close()

    conn.close()
    print('======================================================')
    print('！！！！！！！！print数据删除完毕！！！！！！！！！！！！！')
    print('======================================================')
else:
    cursor.close()

    conn.close()

    print('======================================================')
    print('！！！！！！！！print数据删除完毕！！！！！！！！！！！！！')
    print('======================================================')

