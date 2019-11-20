# -*- coding:utf-8 -*-
# @Desc : 爬虫模块的通用爬虫
# @Author : Administrator
# @Date : 2019-11-18 10:25

import requests
from domain import Proxy
from utils.http import get_request_headers
from lxml import etree


# 安装: pip install lxml


class BaseSpider(object):
    # 代理IP网址的URL列表
    urls = []
    # 分组xpath,获取包含代理IP信息标签列表的XPATH
    group_xpath = ""
    # 组内xpath,获取代理IP详情信息的XPATH,格式: {"ip","xxx", "prot":"xxx"}
    detail_xpath = {}

    def __init__(self, urls=[], group_xpath="", detail_xpath={}):
        """提供初始化方法,传入爬虫的URL列表,分组XPATH,组内(详情)XPATH"""

        if urls:
            self.urls = urls
        if group_xpath:
            self.group_xpath = group_xpath
        if detail_xpath:
            self.detail_xpath = detail_xpath

    def get_page_from_url(self, url):
        """2.根据URL地址发送请求,获取页面数据"""
        res = requests.get(url, headers=get_request_headers())
        print("爬取的网站url地址: %s, 请求状态码: %s" %(res.url, res.status_code))
        # return res.content.decode()  # 报错: UnicodeDecodeError: 'utf-8' codec can't decode byte 0xd4 in position 110: invalid continuation byte
        return res.content  # 二进制数据


    def get_first_from_list(self, lis):
        # 如果列表中有元素就返回第一个,否则返回空串
        return lis[0] if len(lis) != 0 else ""


    def get_proxies_from_page(self, page):
        """3.解析页面,提取数据,封装为Proxy对象"""
        pageElement = etree.HTML(page)  # 可以接受二进制数据

        # 获取包含代理IP信息的标签列表
        trs = pageElement.xpath(self.group_xpath)
        # 遍历trs,获取代理IP相关信息
        for tr in trs:
            # ip = tr.xpath(self.detail_xpath["ip"])[0]
            # port = tr.xpath(self.detail_xpath["port"])[0]
            ip = self.get_first_from_list(tr.xpath(self.detail_xpath["ip"]))
            port = self.get_first_from_list(tr.xpath(self.detail_xpath["port"]))
            proxies = Proxy(ip, port)
            # 使用yiled返回提取到的数据
            yield proxies


    def get_proxies(self):
        """对外提供一个获取代理IP的方法"""
        # 1.遍历URL列表,获取URL
        for url in self.urls:
            # 2.根据URL地址发送请求,获取页面数据
            page = self.get_page_from_url(url)
            # 3.解析页面,提取数据,封装为Proxy对象
            proxies = self.get_proxies_from_page(page)

            # 4.返回Proxy对象列表
            # yield proxies 返回是一个生成器对象, yield from proxies返回的才是Proxy对象
            yield from proxies


if __name__ == '__main__':

    config = {
        # URL列表,列表推导式
        "urls": ["http://www.ip3366.net/free/?stype=1&page={}".format(i) for i in range(1, 4)],
        # 获取分组tr列表
        "group_xpath": '//*[@id="list"]/table/tbody/tr',
        "detail_xpath": {
            "ip": './td[1]/text()',
            "port": './td[2]/text()',
        }
    }

    base = BaseSpider(**config)

    for proxy in base.get_proxies():
        print(proxy)
