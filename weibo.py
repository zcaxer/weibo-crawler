import requests
from bs4 import BeautifulSoup
import json
import webbrowser

uid = 1787905915


def get_followers(uid):
    url_base = 'https://m.weibo.cn/api/container/getIndex'
    param = {'containerid': '231051_-_fans_-_%d' % uid,
             'type': 'all', 'since_id': 1}
    r = requests.get(url_base, param)
    return r
    # webbrowser.open(r.url)


if __name__ == "__main__":
    get_followers(uid)
