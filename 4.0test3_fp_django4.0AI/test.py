from lib.base_conn_sqlite3 import *

session = conn_sqlite3.make_session()
a2 = User(name="uuuu")
session.add(a2)
session.commit()