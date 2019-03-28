# -- coding:utf-8 --
import time

times = time.strftime("%H{y}%M{m}%S{s}").format(y='时', m='分', s='秒')

print(times)