import re
new_text_code1 = 'sp[0]/sp[-1]>1.5'
range_num = re.findall(r'\[(-\d+|\d+)\]', new_text_code1)
print(range_num)