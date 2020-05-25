import json
import math
import random
import webbrowser
from enum import Enum
from time import sleep

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


class containerid(Enum):
    follower = '231051_-_fans_-_{}'
    following = '100505{}_-_FOLLOWERS'
    info = '230283{}_-_INFO'
    like = '230869{}_-_mix'


def get_weibo_api(type, uid, since_id=0, save=0):
    url_getIndex = 'https://m.weibo.cn/api/container/getIndex'
    url_getSecond = 'https://m.weibo.cn/api/container/getSecond'
    param = {'containerid': type.value.format(uid)}
    url_base = ''
    if type == containerid.follower:
        param['since_id'] = since_id
        param['type'] = 'all'
        url_base = url_getIndex
    elif type == containerid.following:
        param["page"] = since_id
        url_base = url_getSecond
    sleep(random.randint(4, 6))
    r = requests.get(url_base, param).json()
    if save != 0:
        f = open("%d_%s_%d.json" % (uid, type, since_id), 'w')
        json.dump(r, f)
        f.close()
    return r


def get_follower_list(uid):
    since_id = 0
    li = []
    flag = 1
    while flag != 0:
        since_id += 1
        r = get_weibo_api(containerid.follower, uid, since_id)
        try:
            cards = r['data']['cards']
        except:
            print("api error")
            break
        if len(cards) == 0:
            flag = 0
            break
        print(since_id)
        for item in cards:
            try:
                j = item['card_group']
                for i in j:
                    try:
                        li.append(i['user']['id'])
                    except:
                        break
            except:
                flag = 0
                break
    print(len(li))
    # print(r.url)
    return li


def get_following_list(uid):
    page = 0
    li = []
    flag = 1
    while flag != 0:
        page += 1
        r = get_weibo_api(containerid.following, uid, page,)
        try:
            cards = r['data']['cards']
        except:
            flag = 0
            break
        if len(cards) == 0:
            flag = 0
            break
        for i in cards:
            try:
                li.append(i['user']['id'])
            except:
                print('no id')
                break
        print(page)

    print(len(li))
    # print(r.url)
    return li


def get_info(uid):
    json = get_weibo_api(containerid.info, uid,save=1)


if __name__ == "__main__":
    li = {}
    j = get_following_list('3318117930')
    for uid in tqdm(j):
    #     print(uid)
    #     li[uid] = (get_following_list(uid))
    # with open("following_list.json", 'w') as f:
    #     json.dump(li, f)
        get_info(uid)