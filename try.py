import json


def parse_userinfo(g, l):

    # ['id', 'screen_name', 'profile_image_url', 'profile_url', 'statuses_count', 'verified', 'verified_type', 'verified_type_ext', 'verified_reason', 'close_blue_v', 'description', 'gender',
        # 'mbtype', 'urank', 'mbrank', 'follow_me', 'following', 'followers_count', 'follow_count', 'cover_image_phone', 'avatar_t', 'cover_image_phone', 'avatar_hd', 'like', 'like_me', 'toolbar_menus']
    if g['ok'] == 1:
        cards = []
        try:
            for i in g['data']['cards']:
                cards += i['card_group']
            for i in cards:
                if i.get('item_name'):
                    if i['item_name'] not in l:
                        l.append(i.get('item_name'))
                    if i['desc'] not in l:
                        l.append(i.get('desc'))
                    if i['desc1'] not in l:
                        l.append(i.get('desc1'))
                    if not i.get('item_content'):
                        print(i['item_name'])
                        print(i['item_content'])
                else:
                    print(i)
        except:
            print('error in parse userInfo')
    return l


li = []
with open(r'ying_following_list', 'r') as f1:
    for line in f1:
        f_index = open(rf'json\{line.rstrip()}_info_0.json', 'r')
        j = json.load(f_index)
        li = parse_userinfo(j, li)
        f_index.close()
print(li)
