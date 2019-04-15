

from lib.base_conn_sqlite3 import *

session = conn_sqlite3.make_session()

sql = "drop table gupiao"   # 解开封印进行删除表

session.execute(sql)      # 解开封印进行删除表