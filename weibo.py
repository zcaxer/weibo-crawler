import json
import math
import random
import webbrowser
from enum import Enum
from time import sleep

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

requests_times = 0


class containerid(Enum):
    follower = '231051_-_fans_-_{}'
    following = '100505{}_-_FOLLOWERS'
    info = '230283{}_-_INFO'
    like = '230869{}_-_mix'


def get_weibo_api(type, uid, since_id=0, save=0):
    url_getIndex = r'https://m.weibo.cn/api/container/getIndex'
    url_getSecond = r'https://m.weibo.cn/api/container/getSecond'
    param = {'containerid': type.value.format(uid)}
    url_base = ''
    if type == containerid.follower:
        param['since_id'] = since_id
        param['type'] = 'all'
        url_base = url_getIndex
    elif type == containerid.following:
        param["page"] = since_id
        url_base = url_getSecond
    elif type == containerid.info:
        url_base = url_getIndex

    global requests_times
    if requests_times > random.randint(1, 4):
        sleep(random.randint(6, 10))
        requests_times = 0
    else:
        requests_times += 1

    s = requests.session()

    headers = {
        'accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    }

    s.headers.update(headers)

    cookie_jar = requests.utils.cookiejar_from_dict({
        '_T_WM': '39162099780',
        'SCF': 'Algm7_7NfHVZ3HUKBUI09UvlHboP5B2tavJy7d9b9R78Nj_Qo4T5VZJEv7Ypa8Vs2lx4pafVwO_I1c3l20suP_Q.',
        'SUB': '_2A25zzvtrDeRhGeFN7FMV8SfNzD6IHXVRMIUjrDV6PUJbkdANLU2hkW1NQ_d6YH2ApgiKse1Rc0ljrtPQ2jujFEE2',
        'SUHB': '0ElKqXzGWiexqF',
        'SSOLoginState': '1590332218',
        'MLOGIN': '1',
        'XSRF-TOKEN': 'd32d06'
    }
    )
    # s.cookies = cookie_jar

    r = s.get(url_base, params=param, cookies=cookie_jar).json()
    if save != 0:
        f = open(r"json\%d_%s_%d.json" % (uid, type.value, since_id), 'w')
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
    json = get_weibo_api(containerid.info, uid, 0, save=1)


if __name__ == "__main__":
    li = {}
    j = get_following_list('3318117930')
    for uid in tqdm(j):
        get_info(uid)
    #     li[uid] = (get_following_list(uid))
    # with open("following_list.json", 'w') as f:
    #     json.dump(li, f)
