# import re

# pa = re.compile(r'\d+\.\d+\.\d+\.\d+')
# li = []
# with open('access.log', 'r') as f:
#     for line in f:
#         ma = pa.search(line)
#         if ma:
#             if ma.group() not in li:
#                 li.append(ma.group())

# print(li)

from enum import Enum


class containerid(Enum):
    follower = '231051_-_fans_-_{}'
    following = '100505{}_-_FOLLOWERS'
    info = '230283{}_-_INFO'
    like = '230869{}_-_mix'


def get_weibo_api(request_type, uid, since_id=0, save=0):

    url_getIndex = 'https://m.weibo.cn/api/container/getIndex'
    url_getSecond = 'https://m.weibo.cn/api/container/getSecond'
    param = {'containerid': request_type.value. format(uid)}
    print(param)


get_weibo_api(containerid.following, 3318117930)
