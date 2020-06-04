import json
import logging

fmt = "%(asctime)-s --%(levelname)s -- %(message)s"
logging.basicConfig(filename='try.log', level=logging.INFO, format=fmt)
logger = logging.getLogger('weibo')


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
                        logger.debug(g['data']['cardlistInfo']
                                     ['containerid'], 'no item_content', i['item_name'])
                    else:
                        pass
                elif i.get('item_type'):
                    name = i['item_type']
                    if name not in l:
                        l.append(name)
                    if not i.get('item_content'):
                        logger.debug(g['data']['cardlistInfo']
                                     ['containerid'], 'no item_content', i['item_type'])
                elif i.get('item_content'):
                    # print(g['data']['cardlistInfo']
                    #       ['containerid'], 'no item name or type', i['item_content'])
                    logger.debug(name, ':', i['item_content'])
                elif i.get('desc'):
                    # print(g['data']['cardlistInfo']['containerid'])
                    # print(i['desc'])
                    # if i['desc'] not in l:
                    #     l.append(i.get('desc'))
                    pass
                elif i.get('desc1'):
                    # if i['desc1'] not in l:
                    #     l.append(i.get('desc1'))
                    pass
                elif i.get('desc2_struct'):
                    # if i['desc1'] not in l:
                    #     l.append(i.get('desc1'))
                    pass
                elif i.get('pics'):
                    # if i['desc1'] not in l:
                    #     l.append(i.get('desc1'))
                    pass
                else:
                    logger.debug(g['data']['cardlistInfo']
                                 ['containerid'], 'not included at', i)

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
