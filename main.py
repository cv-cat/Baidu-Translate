import math
import requests
import execjs
import re
import time

session = requests.Session()
js = execjs.compile(open('baidu.js', 'r', encoding='utf-8').read())
headers = {
    "Referer": "https://fanyi.baidu.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82",
}
params = {
    "from": "en",
    "to": "zh"
}
data = {
    "from": "en",
    "to": "zh",
    "query": "",
    "transtype": "realtime",
    "simple_means_flag": "3",
    "sign": "793638.589591",
    "token": "",
    "domain": "common",
    "ts": 1
}
url = "https://fanyi.baidu.com/"
translate_url = "https://fanyi.baidu.com/v2transapi"
response = session.get(url, headers=headers,)
if response.cookies:
    print('获取cookies成功')
# 需要请求两次，第一次获取cookies
response = session.get(url, headers=headers,)
token = re.findall(r"token: '(.*?)',", response.text)[0]
gtk = re.findall(r'window.gtk = "(.*?)";', response.text)[0]
data['token'] = token

def translate(query):
    data['query'] = query
    data['ts'] = math.floor(time.time() * 1000)
    sign = js.call('getsign', query, gtk)
    data['sign'] = sign
    response = session.post(translate_url, headers=headers, params=params, data=data)
    text = response.json()
    print(text['trans_result']['data'][0]['dst'])

translate('hello')
