# -*- coding:utf-8 -*-
# @Desc :  代理池的校验模块
# @Author : Administrator
# @Date : 2019-11-18 10:22

import time
import json
import settings
import requests
from utils.log import logger
from utils import http
from domain import Proxy



def check_proxy(proxy):
    '''检测指定的 代理IP,响应速度, 匿名程度, 支持协议类型'''

    # 根据proxy对象构造,请求使用的代理
    proxies = {
        "http": "http://{}:{}".format(proxy.ip, proxy.port),
        "https": "https://{}:{}".format(proxy.ip, proxy.port),
    }

    # 测试该代理IP
    # http, http_nick_type, http_speed = _check_http_proxy(proxies)
    # https, https_nick_type, https_speed = _check_http_proxy(proxies, False)

    http = _check_http_proxy(proxies)
    https = _check_http_proxy(proxies, False)

    if http and https:
        # 如果http和https都可以请求成功,说明支持两种协议,协议类型为2
        proxy.protocol = 2
        # proxy.nick_type = http_nick_type
        # proxy.speed = http_speed
    elif http:
        # 如果只有http可以请求成功,说明支持http协议,协议类型为0
        proxy.protocol = 0
        # proxy.nick_type = http_nick_type
        # proxy.speed = http_speed
    elif https:
        # 如果只有https可以请求成功,说明支持https协议,协议类型为1
        proxy.protocol = 1
        # proxy.nick_type = https_nick_type
        # proxy.speed = https_speed
    else:
        proxy.protocol = -1
        # proxy.nick_type = -1
        # proxy.speed = -1

    logger.debug(proxy)
    return proxy


def _check_http_proxy(proxies, is_http=True):
    # nick_type = -1  # 匿名程度: 高匿 0, 匿名 1, 透明 2
    # speed = -1  # 响应速度,单位秒

    if is_http:
        test_url = "http://httpbin.org/get"
    else:
        test_url = "https://httpbin.org/get"

    try:
        # 获取开始时间
        # start = time.time()
        # 发送请求,获取响应数据
        res = requests.get(url=test_url, headers=http.get_request_headers(), timeout=settings.TEST_TIMEOUT, proxies=proxies)
        # print("------- 请求状态码: %s" %res.status_code)
        if res.ok:  # 说明响应成功
        # if res.status_code == 200:  # 说明响应成功
            # 计算响应速度,保留两位小数
            # speed = round(time.time() - start, 2)
            # 把响应内容转换为字典数据
            # content = json.loads(res.text)

            # 匿名程度
            # 获取origin,请求来源的IP地址
            # origin = content["origin"]
            # 获取请求中Proxy-Connection,如果有,说明是匿名代理
            # proxy_connection = res.get("Proxy-Connection", None)

            # if "," in origin:
            #     # 如果origin中有,逗号分割的两个IP就是透明代理IP,
            #     nick_type = 2  # 透明
            # elif proxy_connection:
            #     # 如果headers中含有Proxy-Connection说明是匿名代理
            #     nick_type = 1  # 匿名
            # else:
            #     # 否则就是高匿代理IP
            #     nick_type = 0  # 高匿
            # return True, nick_type, speed

            return True

        else:
            # return False, nick_type, speed  # False, nick_type=-1, speed=-1
            return False

    except Exception as e:
        # logger.exception(e)
        # return False, nick_type, speed  # False, nick_type=-1, speed=-1
        if is_http:
            print("******* HTTP请求出现错误!")
        else:
            print("******* HTTPS请求出现错误!")
        return False



if __name__ == "__main__":
    proxy = Proxy(ip="180.158.11.89", port="58080")
    res = check_proxy(proxy)  # res为Proxy的对象
    # print(res.__dict__)








