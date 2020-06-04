# -*- coding: UTF-8
import json
import logging

fmt = "%(asctime)-s - %(levelname)s - %(message)s"
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
                if 'item_name' in i:
                    name = i['item_name']
                    if name not in l:
                        l.append(name)
                        logger.debug("%s first item_name appeares in %s", name, i)
                    if not 'item_content' in i:
                        logger.info("json %s's item_name :%s has no item_content", g['data']['cardlistInfo']
                        ['containerid'], i['item_name'])
                elif 'item_type' in i:
                    name = i['item_type']
                    if name not in l:
                        l.append(name)
                        logger.debug("%s first item_type appeares in %s", name, i)
                    if not 'item_content' in i:
                        logger.info()("json %s's item_type :%s has no item_content", g['data']['cardlistInfo']
                        ['containerid'], i['item_type'])
                elif 'item_content' in i:
                    # print(g['data']['cardlistInfo']
                    #       ['containerid'], 'no item name or type', i['item_content'])
                    logger.info("json %s's item_type item_content %s has no item_name,last item_name is %s",
                                 g['data']['cardlistInfo']['containerid'], i['item_content'], name)
                elif 'desc' in i:
                    logger.info("json %s  has 'desc':%s",
                                 g['data']['cardlistInfo']['containerid'], i['desc'])
                    # if i['desc'] not in l:
                    #     l.append(i.get('desc'))

                elif 'desc1' in i:
                    logger.info("json %s  has 'desc1':%s",
                                 g['data']['cardlistInfo']['containerid'], i['desc1'])
                elif 'desc2_struct' in i:
                    # if i['desc2_struct'] not in l:
                    #     l.append(i.get('desc2_struct'))
                    logger.info("json %s  has 'desc2_struct':%s",
                                 g['data']['cardlistInfo']['containerid'], i['desc2_struct'])
                elif 'pics' in i:
                    # if i['pics'] not in l:
                    #     l.append(i.get('pics'))
                    logger.info("json %s  has 'pics':%s",
                                 g['data']['cardlistInfo']['containerid'], i['pics'])
                else:
                    logger.warning('%s has field not included :\n %s', g['data']['cardlistInfo']
                    ['containerid'], i)

        except:
            logger.warning('error in parse %s',g['data']['cardlistInfo']['containerid'])
    return l


li = []
with open(r'ying_following_list', 'r') as f1:
    for line in f1:
        f_info = open(rf'json\{line.rstrip()}_info_0.json', 'r')
        j = json.load(f_info)
        li = parse_userInfo(j, li)
        f_info.close()

# f = open(r'C:\Users\zcaxe\workspace\python\weibo\json\5234367848_info_0.json','r')
# j=json.load(f)
# parse_userInfo(j,li)
print(li)
