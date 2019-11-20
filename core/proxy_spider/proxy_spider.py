# -*- coding:utf-8 -*-
# @Desc : 具体爬虫类模块
# @Author : Administrator
# @Date : 2019-11-18 10:23

from core.proxy_spider.base_spider import BaseSpider
import time
import random

"""
1. 实现西刺代理IP爬虫: https://www.xicidaili.com/nn/1
    定义一个类继承通用爬虫类(BaseSpider)
    提供urls, group_xpath, detail_xpath
"""
class XiciSpider(BaseSpider):

    # 准备URL列表
    urls = ["https://www.xicidaili.com/nn/{}".format(i) for i in range(1, 11)]

    # 分组xpath,获取包含代理IP信息标签列表的XPATH
    group_xpath = '//*[@id="ip_list"]/tr[position()>1]'

    # 组内xpath,获取代理IP详情信息的XPATH,格式: {"ip","xxx", "prot":"xxx"}
    detail_xpath = {
        "ip": "./td[2]/text()",
        "port": "./td[3]/text()",
    }


"""
2. 实现快代理代理IP爬虫: https://www.kuaidaili.com/free/inha/1/
    定义一个类继承通用爬虫类(BaseSpider)
    提供urls, group_xpath, detail_xpath
"""
class KuaidailiSpider(BaseSpider):

    # 准备URL列表
    urls = ["https://www.kuaidaili.com/free/inha/{}".format(i) for i in range(1, 6)]

    # 分组xpath,获取包含代理IP信息标签列表的XPATH
    group_xpath = '//*[@id="list"]/table/tbody/tr'

    # 组内xpath,获取代理IP详情信息的XPATH,格式: {"ip","xxx", "prot":"xxx"}
    detail_xpath = {
        "ip": "./td[1]/text()",
        "port": "./td[2]/text()",
    }

    # 当两个url地址页面访问时间间隔太短,就会报错,这是一种反爬手段
    def get_page_from_url(self, url):
        # 随机等待1到3秒
        time.sleep(random.uniform(1,3))
        # 调用父类的这个方法, 发送请求,获取响应数据
        return super().get_page_from_url(url)


"""
3. 实现ip3366代理IP爬虫: http://www.ip3366.net/free/?stype=1&page=2
    定义一个类继承通用爬虫类(BaseSpider)
    提供urls, group_xpath, detail_xpath
"""
class Ip3366Spider(BaseSpider):

    # 准备URL列表
    urls = ["http://www.ip3366.net/?stype={}&page={}".format(i, j) for i in range(1, 3) for j in range(1, 11)]

    # 分组xpath,获取包含代理IP信息标签列表的XPATH
    group_xpath = '//*[@id="list"]/table/tbody/tr'

    # 组内xpath,获取代理IP详情信息的XPATH,格式: {"ip","xxx", "prot":"xxx"}
    detail_xpath = {
        "ip": "./td[1]/text()",
        "port": "./td[2]/text()",
    }

    # 当两个url地址页面访问时间间隔太短,就会报错,这是一种反爬手段
    def get_page_from_url(self, url):
        # 随机等待1到3秒
        time.sleep(random.uniform(1,3))
        # 调用父类的这个方法, 发送请求,获取响应数据
        return super().get_page_from_url(url)



if __name__ == '__main__':

    # 西刺爬虫
    # spider = XiciSpider()
    # print(spider.urls)

    # ip3366爬虫
    spider = Ip3366Spider()
    # print(spider.urls)

    # 快代理
    # spider = KuaidailiSpider()
    # print(spider.urls)

    for proxy in spider.get_proxies():
        print(proxy)
