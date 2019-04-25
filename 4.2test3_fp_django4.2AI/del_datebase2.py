from lib.second_conn_sqlite3 import *

session = second_conn_sqlite3.make_session()

sql = "drop table gupiao_second"   # 解开封印进行删除表

session.execute(sql)      # 解开封印进行删除表