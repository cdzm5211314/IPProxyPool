# -*- coding:utf-8 -*-
# @Desc : 代理池的数据库模块
# @Author : Administrator
# @Date : 2019-11-19 9:45

# 安装: pip install pymongo

from pymongo import MongoClient
from settings import MONGO_URL
from utils.log import logger
from domain import Proxy

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
        self.proxies.update_one({"_id":proxy.ip}, {"$set":proxy.__dict__})

    def delete_one(self,proxy):
        '''删除一条集合数据,根据IP删除代理IP数据'''
        self.proxies.delete_one({"_id":proxy.ip})
        logger.info("已删除代理IP:{}".format(proxy))

    def find_all(self):
        '''查询集合中所有代理IP的功能'''
        cursor = self.proxies.find()  # 列表
        for item in cursor:  # item字典
            item.pop("_id")  # 删除item字典的_id这个key
            proxy = Proxy(**item)
            yield  proxy



if __name__ == '__main__':

    mongo = MongoPool()

    # proxy = Proxy(ip="211.147.226.4", port="8118")
    # mongo.insert_one(proxy)

    # proxy = Proxy(ip="211.147.226.4", port="8888")
    # mongo.update_one(proxy)

    # proxy = Proxy(ip="211.147.226.4", port="8118")
    # mongo.delete_one(proxy)

    for proxy in mongo.find_all():
        print(proxy)

