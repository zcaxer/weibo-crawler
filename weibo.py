import requests
from bs4 import BeautifulSoup
import json
import webbrowser
from time import sleep
import math
import random
from tqdm import tqdm
from enum import Enum


class containerid(Enum):
    follower = '231051_-_fans_-_%d'
    following = '100505%d_-_FOLLOWERS'
    info = '230283%d_-_INFO'
    like = '230869%d_-_mix'



def get_weibo_api(type, uid, since_id, save=0):
    url_getIndex = 'https://m.weibo.cn/api/container/getIndex'
    url_getSecond = 'https://m.weibo.cn/api/container/getSecond'
    param = {'containerid':type%uid}
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
    json=get_weibo_api(containerid.info,uid)

    


if __name__ == "__main__":
    li = {}
    j = get_follower_list(2835933097)
    for uid in tqdm(j):
        li[uid] = (get_following_list(uid))
    with open("following_list.json", 'w') as f:
        json.dump(li, f)

