import requests

uid = 1192843505
url = f"https://m.weibo.cn/api/container/getIndex?containerid=230283{uid}"
s = requests.session()

payload = {}
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

response = s.get(url, cookies=cookie_jar)


print(response.text.encode('utf8'))
