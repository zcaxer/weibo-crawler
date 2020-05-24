import re

pa = re.compile(r'\d+\.\d+\.\d+\.\d+')
li = []
with open('access.log', 'r') as f:
    for line in f:
        ma = pa.search(line)
        if ma:
            if ma.group() not in li:
                li.append(ma.group())

print(li) 