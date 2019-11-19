# -*- coding:utf-8 -*-
# @Desc : 代理池的数据库模块
# @Author : Administrator
# @Date : 2019-11-19 9:45

# 安装: pip install pymongo

from pymongo import MongoClient
from settings import MONGO_URL
from utils.log import logger
from domain import Proxy
from random import choice


class MongoPool(object):

    def __init__(self):
        '''建立数据库链接,获取要操作的集合'''
        self.client = MongoClient(MONGO_URL)  # 链接数据库
        self.proxies = self.client["proxies_pool"]["proxies"]  # 操作的集合

    def __del__(self):
        '''关闭数据库链接'''
        self.client.close()

    def insert_one(self, proxy):
        '''插入一条数据到集合'''
        # 查看此代理IP是否存在集合中
        count = self.proxies.count_documents({"_id": proxy.ip})
        if count == 0:  # 集合中不存在此代理
            # 使用proxy.ip作为MongoDB数据库集合的主键: _id
            dic = proxy.__dict__  # 转换proxy对象数据为字典类型数据
            dic["_id"] = proxy.ip
            self.proxies.insert_one(dic)
            logger.info("插入代理IP:{}".format(proxy.ip))

        else:
            logger.warning("已经存在的代理IP:{}".format(proxy.ip))

    def update_one(self, proxy):
        '''修改一条集合数据'''
        self.proxies.update_one({"_id": proxy.ip}, {"$set": proxy.__dict__})

    def delete_one(self, proxy):
        '''删除一条集合数据,根据IP删除代理IP数据'''
        self.proxies.delete_one({"_id": proxy.ip})
        logger.info("已删除代理IP:{}".format(proxy))

    def find_all(self):
        '''查询集合中所有代理IP的功能'''
        cursor = self.proxies.find()  # 列表
        for item in cursor:  # item字典
            item.pop("_id")  # 删除item字典的_id这个key
            proxy = Proxy(**item)
            yield proxy

    def find(self, conditions={}, count=0):
        """
        根据条件进行查询,指定查询条件,分数值降序
        :param conditions: 查询条件字典
        :param count: 限制最多取出多少个代理IP,默认获取所有
        :return: 返回满足要求代理IP(Proxy对象)列表
        """
        cursor = self.proxies.find(conditions, limit=count).sort("score", -1)
        # 准备列表,用来存储查询处理代理IP
        proxy_list = []
        for item in cursor:
            item.pop("_id")
            proxy = Proxy(**item)
            proxy_list.append(proxy)

        return proxy_list

    def get_proxies(self, protocol=None, domain=None, count=0):
        """
        根据协议类型 和 要访问网站的域名,获取代理IP
        :param protocol: 协议类型 http 0, https 1, http&https 2
        :param domain: 域名 jd.com
        :param count: 限制最多取出多少个代理IP,默认获取所有
        :return: 返回满足要求代理IP(Proxy对象)列表
        """
        # 准备列表,用来存储查询处理代理IP
        proxy_list = []

        # 定义查询条件
        conditions = {}
        # 根据协议类型,指定查询条件
        if protocol is None:  # 如果没有传入协议类型,返回支持http和https协议的代理IP
            conditions["protocol"] = 2
        elif protocol.lower() == "http":
            conditions["protocol"] = {"$in": [0, 2]}
        else:
            conditions["protocol"] = {"$in": [1, 2]}

        if domain:
            conditions["disable_domains"] = {"$nin": [domain]}

        for proxy in self.proxies.find(conditions, limit=count):
            proxy_list.append(proxy)

        return proxy_list

    def random_proxy(self, protocol=None, domain=None, count=0):
        """
        根据协议类型 和 要访问网站的域名,随机获取代理IP
        :param protocol: 协议类型 http 0, https 1, http&https 2
        :param domain: 域名 jd.com
        :param count: 限制最多取出多少个代理IP,默认获取所有
        :return: 返回满足要求的随机的一个代理IP(Proxy对象)
        """

        # 准备列表,用来存储查询处理代理IP
        proxy_list = []
        for proxy in self.get_proxies(protocol=protocol, domain=domain, count=count):
            proxy_list.append(proxy)

        return choice(proxy_list)

    def disable_doamin(self, ip, domain):
        """
        把指定域名添加到指定代理IP的disable_domains列表中
        :param ip: IP地址
        :param domain: 域名
        :return: 如果返回True,添加成功,否则反之
        """
        count = self.proxies.count_documents({"_id":ip, "disable_domains": domain})
        if count == 0:
            # 如果这个disable_domain中没有这个域名,才添加
            self.proxies.update_one({"_id": ip}, {"$push": {"disable_domains": domain}})
            return True

        return False

if __name__ == '__main__':
    mongo = MongoPool()

    # proxy = Proxy(ip="211.147.226.4", port="8118")
    # mongo.insert_one(proxy)

    # dic = {'ip': '192.168.208.100', 'port': '58080', 'protocol': 1, 'score': 40, 'disable_domains': []}
    # dic = {'ip': '192.168.208.101', 'port': '1080', 'protocol': 0, 'score': 50, 'disable_domains': []}
    # dic = {'ip': '192.168.208.102', 'port': '9797', 'protocol': 2, 'score': 30, 'disable_domains': []}
    # dic = {'ip': '192.168.208.103', 'port': '9999', 'protocol': 2, 'score': 20, 'disable_domains': []}
    # dic = {'ip': '192.168.208.104', 'port': '9999', 'protocol': 0, 'score': 10, 'disable_domains': []}
    # proxy = Proxy(**dic)
    # mongo.insert_one(proxy)

    # proxy = Proxy(ip="211.147.226.4", port="8888")
    # mongo.update_one(proxy)

    # proxy = Proxy(ip="211.147.226.4", port="8118")
    # mongo.delete_one(proxy)

    # for proxy in mongo.find_all():
    #     print(proxy)

    # for proxy in mongo.find():
    # for proxy in mongo.find({"protocol":-1}, 5):
    #     print(proxy)

    # for proxy in mongo.get_proxies():
    # for proxy in mongo.get_proxies("HTTP", 3):
    #     print(proxy)

    # proxy = mongo.random_proxy()
    # print(proxy)

    # mongo.disable_doamin("192.168.208.102", "baidu.com")