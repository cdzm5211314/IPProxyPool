# -*- coding:utf-8 -*-
# @Desc : 获取随机User-Agent请求头
# @Author : Administrator
# @Date : 2019-11-18 10:26

import random

# from fake_useragent import UserAgent
# ua = UserAgent()

# 1.准备User-Agent列表
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50",
]


# 2.实现一个方法,获取随机的User-Agent请求头
def get_request_headers():
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        # "User-Agent": ua.chrome,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9",
        # "Accept-Language": "en_US,en;q=0.5",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate",
    }

    return headers


if __name__ == '__main__':
    print(get_request_headers())
    print(get_request_headers())
    print(get_request_headers())
    print(get_request_headers())
    print(get_request_headers())
