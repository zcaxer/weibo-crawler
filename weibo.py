import requests
from bs4 import BeautifulSoup
import json
import webbrowser
from time import sleep
import math
import random

follower = '231051_-_fans_-_%d'
following = '231051_-_followers_-_%d'


def get_weibo_api(type, uid, since_id, save=0):
    url_base_follower = 'https://m.weibo.cn/api/container/getIndex'
    url_base_following = 'https://m.weibo.cn/api/container/getSecond'
    url_base_info=''
    param = {}
    url_base = ''
    if type == follower:
        param['since_id'] = since_id
        param['containerid'] = type % uid
        param['type'] = 'all'
        url_base = url_base_follower
    elif type == following:
        param["page"] = since_id
        param['containerid'] = '100505%d_-_FOLLOWERS' % uid
        url_base = url_base_following
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
        r = get_weibo_api(follower, uid, since_id)
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
        r = get_weibo_api(following, uid, page,)
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


j = get_following_list(6299499718)
print(j)
