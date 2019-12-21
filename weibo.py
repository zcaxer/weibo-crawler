import requests
from bs4 import BeautifulSoup
import json
import webbrowser
follower = '231051_-_fans_-_%d'
following = '231051_-_followers_-_%d'


def get_weibo_api(type, uid, since_id, save=0):
    url_base = 'https://m.weibo.cn/api/container/getIndex'
    param = {'containerid':  type % uid,
             'type': 'all', 'since_id': since_id}
    r = requests.get(url_base, param).json()
    if save != 0:
        f = open("%d_followers_%d.json" % (uid, since_id), 'w')
        json.dump(r, f)
        f.close()
    return r


def get_follower_list(uid):
    since_id = 0
    li = []
    while 1:
        since_id += 1
        r = get_weibo_api(follower, uid, since_id, 1)
        try:
            j = r['data']['cards'][0]['card_group']
        except:
            break
        print(since_id)
        for i in j:
            li.append(i['user']['id'])
    print(len(li))
    # print(r.url)
    return li


def get_following_list(uid):
    since_id = 0
    li = []
    while 1:
        since_id += 1
        r = get_weibo_api(following, uid, since_id, 1)
        try:
            j = r['data']['cards'][0]['card_group']
        except:
            break
        print(since_id)
        for i in j:
            li.append(i['user']['id'])
    print(len(li))
    # print(r.url)
    return li


j = get_follower_list(6299499718)
print(j)
