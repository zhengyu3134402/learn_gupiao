
import time

start1_time = time.time()

start1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start1_time)) # 开始时间


end1_time = time.time()
end1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end1_time)) # 结束时间

hua1 = end1_time - start1_time