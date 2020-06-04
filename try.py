# -*- coding: UTF-8
import json
import logging

fmt = "%(asctime)-s --%(levelname)s -- %(message)s"
logger = logging.getLogger('weibo')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('try.log', 'w', "UTF-8")
handler.setFormatter(logging.Formatter(fmt))
logger.addHandler(handler)


def parse_userInfo(g, l):
    # ['id', 'screen_name', 'profile_image_url', 'profile_url', 'statuses_count', 'verified', 'verified_type', 'verified_type_ext', 'verified_reason', 'close_blue_v', 'description', 'gender',
    # 'mbtype', 'urank', 'mbrank', 'follow_me', 'following', 'followers_count', 'follow_count', 'cover_image_phone', 'avatar_t', 'cover_image_phone', 'avatar_hd', 'like', 'like_me', 'toolbar_menus']
    if g['ok'] == 1:
        cards = []
        try:
            name = ''
            for i in g['data']['cards']:
                cards += i['card_group']
            for i in cards:
                if i.get('item_name'):
                    name = i['item_name']
                    if name not in l:
                        l.append(name)
                    if not i.get('item_content'):
                        logger.debug("json %s's item_name :%s has no item_content", g['data']['cardlistInfo']
                        ['containerid'], i['item_name'])
                    else:
                        pass
                elif i.get('item_type'):
                    name = i['item_type']
                    if name not in l:
                        l.append(name)
                    if not i.get('item_content'):
                        logger.debug("json %s's item_type :%s has no item_content", g['data']['cardlistInfo']
                        ['containerid'], i['item_type'])
                elif i.get('item_content'):
                    # print(g['data']['cardlistInfo']
                    #       ['containerid'], 'no item name or type', i['item_content'])
                    logger.debug("json %s's item_type item_content %s has no item_name,last item_name is %s",
                                 g['data']['cardlistInfo']['containerid'], i['item_content'], name)
                elif i.get('desc'):
                    logger.debug("json %s  has 'desc':%s",
                                 g['data']['cardlistInfo']['containerid'], i['desc'])
                    # if i['desc'] not in l:
                    #     l.append(i.get('desc'))

                elif i.get('desc1'):
                    logger.debug("json %s  has 'desc1':%s",
                                 g['data']['cardlistInfo']['containerid'], i['desc1'])
                elif i.get('desc2_struct'):
                    # if i['desc2_struct'] not in l:
                    #     l.append(i.get('desc2_struct'))
                    logger.debug("json %s  has 'desc2_struct':%s",
                                 g['data']['cardlistInfo']['containerid'], i['desc2_struct'])
                elif i.get('pics'):
                    # if i['pics'] not in l:
                    #     l.append(i.get('pics'))
                    logger.debug("json %s  has 'pics':%s",
                                 g['data']['cardlistInfo']['containerid'], i['pics'])
                else:
                    logger.debug('%s has field not included :\n %s', g['data']['cardlistInfo']
                    ['containerid'], i)

        except:
            logger.warning('error in parse userInfo')
    return l


li = []
with open(r'ying_following_list', 'r') as f1:
    for line in f1:
        f_info = open(rf'json\{line.rstrip()}_info_0.json', 'r')
        j = json.load(f_info)
        li = parse_userInfo(j, li)
        f_info.close()
print(li)
