import json
import logging
import math
import random
import webbrowser
from enum import Enum
from time import sleep

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

requests_times = 0

fmt = "%(asctime)-s --%(levelname)s -- %(message)s"
logging.basicConfig(filename='weibo.log', level=logging.INFO, format=fmt)
logger = logging.getLogger('weibo')


class Containerid(Enum):
    follower = '231051_-_fans_-_{}'
    following = '100505{}_-_FOLLOWERS'
    main_page = '100505{}'
    profile = '230283{}'
    info = '230283{}_-_INFO'
    like = '230869{}_-_mix'


def create_session():
    s = requests.session()

    headers = {
        'accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/81.0.4044.138 Safari/537.36 '
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
    s.cookies = cookie_jar
    return s


def get_weibo_api(type, uid, session, since_id=0, save=0):
    url_getIndex = r'https://m.weibo.cn/api/container/getIndex'
    url_getSecond = r'https://m.weibo.cn/api/container/getSecond'
    param = {'containerid': type.value.format(uid)}
    url_base = url_getIndex
    if type == Containerid.follower:
        param['since_id'] = since_id
        param['type'] = 'all'
    elif type == Containerid.following:
        param["page"] = since_id
        url_base = url_getSecond

    global requests_times
    if requests_times > 0:
        sleep(random.randint(5, 7))
        requests_times = 0
    else:
        requests_times += 1

    # TODO 判断错误类型后，重试或等待ip恢复，在出现意外错误是保留数据
    try:
        response = session.get(url_base, params=param)
        try:
            j = response.json()
            if j['ok']:
                if save != 0:
                    f = open(r"json\%d_%s_%d.json" %
                             (uid, type.name, since_id), 'w')
                    json.dump(j, f)
                    f.close()
                return j
            else:
                logger.warning(f'{uid}_{type.name} json not ok')
                return response
        except:
            logger.warning(f'{uid}_{type.name} json failed')
            return response
    except:
        logger.warning(f'{uid}_{type.name} response  failed')
    return None


def get_follower_list(uid):
    since_id = 0
    li = []
    flag = 1
    while flag != 0:
        since_id += 1
        r = get_weibo_api(Containerid.follower, uid, since_id)
        try:
            cards = r['data']['cards']
        except:
            logger.warning("api error")
            break
        if len(cards) == 0:
            flag = 0
            break
        logger.info(f'crawling following_list page: {since_id}')
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
    logger.info(f"crawled uid's {len(li)} following id")
    # print(r.url)
    return li


def get_following_list(uid):
    page = 0
    li = []
    flag = 1
    while flag != 0:
        page += 1
        r = get_weibo_api(Containerid.following, uid, page, )
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
                logger.warning('no id')
                break
        logger.info('crawling  follower page: {page}')

    logger.info(f"crawled uid's {len(li)} follower id")
    # print(r.url)
    return li


def get_info(uid):
    s = create_session
    get_weibo_api(Containerid.main_page, uid, s, save=1)
    get_weibo_api(Containerid.info, uid, s, save=1)


def parse_userinfo(g, l):
    # ['id', 'screen_name', 'profile_image_url', 'profile_url', 'statuses_count', 'verified', 'verified_type', 'verified_type_ext', 'verified_reason', 'close_blue_v', 'description', 'gender',
    # 'mbtype', 'urank', 'mbrank', 'follow_me', 'following', 'followers_count', 'follow_count', 'cover_image_phone', 'avatar_t', 'cover_image_phone', 'avatar_hd', 'like', 'like_me', 'toolbar_menus']
    if g['ok'] == 1:
        try:
            info_dic = g['data']['userInfo']
            for i in info_dic:
                if i not in l:
                    l.append(i)
        except:
            logger.warning('error in parse userInfo')
    return l


if __name__ == "__main__":
    li = []
    # j = get_following_list('3318117930')
    # for uid in tqdm(j):
    #     get_info(uid)
    # #     li[uid] = (get_following_list(uid))
    # # with open("following_list.json", 'w') as f:
    # #     json.dump(li, f)
    with open(r'ying_following_list', 'r') as f1:
        for line in f1:
            # logger.info(line)
            f_index = open(rf'json\{line.rstrip()}_index_0.json', 'r')
            j = json.load(f_index)
            li = parse_userinfo(j, li)
            f_index.close()
    print(li)
