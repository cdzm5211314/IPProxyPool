# -*- coding:utf-8 -*-
# @Desc : 运行爬虫模块
# @Author : Administrator
# @Date : 2019-11-18 10:23

# 目的: 根据配置文件信息,加载爬虫,抓取代理IP,进行校验,如果ip可用就写入到数据库中


# 打猴子补丁
# 安装: pip install gevent
from gevent import monkey
monkey.patch_all()
# 导入协程池
from gevent.pool import Pool


# 安装: pip install schedule
import schedule
import time

from settings import PROXIES_SPIDERS, RUN_SPIDRS_INTERVAL
from core.proxy_validate.httpbin_validator import check_proxy
from core.db.mongo_pool import MongoPool
from utils.log import logger
import importlib


# 第三种方式: schedule模块
class RunSpider(object):

    def __init__(self):
        # 创建MongoPool代理池对象
        self.mongo_pool = MongoPool()

    def get_spider_from_settings(self):
        """根据配置文件信息,获取爬虫对象列表(即具体的爬虫类对象列表)"""
        # 遍历配置文件中的爬虫信息,获取每个爬虫的全类名
        for full_class_name in PROXIES_SPIDERS:
            # 根据全类名信息创建每个爬虫类对象
            # 如根据全类名 core.proxy_spider.proxy_spider.XiciSpider
            # 获取 模块名和类名
            module_name, class_name = full_class_name.rsplit(".", maxsplit=1)  # 根据右边的第一个"."进行截取,maxsplit=1表示截取一次
            # print(full_class_name.rsplit(".", maxsplit=1))  # ['core.proxy_spider.proxy_spider', 'XiciSpider']
            # print(module_name, class_name)

            # 根据模块名 导入 模块, 动态导入模块
            module = importlib.import_module(module_name)
            # 根据类名,从模块中获取类
            cls = getattr(module, class_name)
            # 根据类,创建爬虫对象
            spider = cls()
            # print(spider)
            yield spider

    def run(self):
        """1. 提供一个运行爬虫的run方法,作为运行爬虫的入口,实现核心的处理逻辑"""

        # 2.1 根据配置文件信息,获取爬虫对象列表(即具体的爬虫类对象列表)
        spiders = self.get_spider_from_settings()

        # 2.2 遍历爬虫对象列表,获取爬虫对象,遍历爬虫对象的get_proxies方法,获取代理IP
        for spider in spiders:
            # 2.5 处理异常,防止一个爬虫内部出错,影响其他的爬虫
            try:
                # 遍历爬虫对象的get_proxies方法,获取代理IP
                for proxy in spider.get_proxies():
                    # print(type(proxy), proxy)

                    # 2.3 检测代理IP(代理IP检测模块:httpbin_validator.py)
                    proxy = check_proxy(proxy)

                    # 2.4 如果IP可用,写入数据库(数据库模块: mongo_pool.py)
                    # 如果protocol不等于-1,说明IP可用
                    if proxy.protocol != -1:
                        # 把可用IP写入到数据库
                        self.mongo_pool.insert_one(proxy)
            except Exception as e:
                # 爬虫报错,记录日志信息
                logger.exception(e)

    # 4.1 定义一个start的类方法
    @classmethod
    def start(cls):
        # 4.2 创建当前类的对象,调用run方法
        rs = RunSpider()
        rs.run()

        # 4.3 使用schedule模块,每隔一定的时间,执行当前对象的run方法
        # 修改配置文件,增加爬虫运行时间间隔的配置,单位为小时
        schedule.every(RUN_SPIDRS_INTERVAL).hours.do(rs.run())
        while True:
            schedule.run_pending()
            time.sleep(1)



# 第二种方式: 使用异步
# class RunSpider(object):
#
#     def __init__(self):
#         # 创建MongoPool代理池对象
#         self.mongo_pool = MongoPool()
#
#         # 3.1 创建协程池对象
#         self.coroutine_pool = Pool()
#
#     def get_spider_from_settings(self):
#         """根据配置文件信息,获取爬虫对象列表(即具体的爬虫类对象列表)"""
#         # 遍历配置文件中的爬虫信息,获取每个爬虫的全类名
#         for full_class_name in PROXIES_SPIDERS:
#             # 根据全类名信息创建每个爬虫类对象
#             # 如根据全类名 core.proxy_spider.proxy_spider.XiciSpider
#             # 获取 模块名和类名
#             module_name, class_name = full_class_name.rsplit(".", maxsplit=1)  # 根据右边的第一个"."进行截取,maxsplit=1表示截取一次
#             # print(full_class_name.rsplit(".", maxsplit=1))  # ['core.proxy_spider.proxy_spider', 'XiciSpider']
#             # print(module_name, class_name)
#
#             # 根据模块名 导入 模块, 动态导入模块
#             module = importlib.import_module(module_name)
#             # 根据类名,从模块中获取类
#             cls = getattr(module, class_name)
#             # 根据类,创建爬虫对象
#             spider = cls()
#             # print(spider)
#             yield spider
#
#
#     def run(self):
#         """1. 提供一个运行爬虫的run方法,作为运行爬虫的入口,实现核心的处理逻辑"""
#         # 2.1 根据配置文件信息,获取爬虫对象列表(即具体的爬虫类对象列表)
#         spiders = self.get_spider_from_settings()
#
#         # 2.2 遍历爬虫对象列表,获取爬虫对象,遍历爬虫对象的get_proxies方法,获取代理IP
#         for spider in spiders:
#
#             # 2.5 处理异常,防止一个爬虫内部出错,影响其他的爬虫
#             # self.__execute_one_spider_task(spider)
#
#             # 3.3 使用异步方式执行这个方法
#             self.coroutine_pool.apply_async(self.__execute_one_spider_task, args=(spider,))
#
#         # 3.4 调用协程的join方法,让当前线程等待 协程 任务的完成
#         self.coroutine_pool.join()
#
#
#     def __execute_one_spider_task(self, spider):
#         """3.2 把处理一个代理爬虫的代码抽取到一个方法中"""
#         try:
#             # 遍历爬虫对象的get_proxies方法,获取代理IP
#             for proxy in spider.get_proxies():
#                 # print(type(proxy), proxy)
#
#                 # 2.3 检测代理IP(代理IP检测模块:httpbin_validator.py)
#                 proxy = check_proxy(proxy)
#
#                 # 2.4 如果IP可用,写入数据库(数据库模块: mongo_pool.py)
#                 # 如果protocol不等于-1,说明IP可用
#                 if proxy.protocol != -1:
#                     # 把可用IP写入到数据库
#                     self.mongo_pool.insert_one(proxy)
#         except Exception as e:
#             # 爬虫报错,记录日志信息
#             logger.exception(e)


# 第一种方式: run() 方法
# class RunSpider(object):
#
#     def __init__(self):
#         # 创建MongoPool代理池对象
#         self.mongo_pool = MongoPool()
#
#     def get_spider_from_settings(self):
#         """根据配置文件信息,获取爬虫对象列表(即具体的爬虫类对象列表)"""
#         # 遍历配置文件中的爬虫信息,获取每个爬虫的全类名
#         for full_class_name in PROXIES_SPIDERS:
#             # 根据全类名信息创建每个爬虫类对象
#             # 如根据全类名 core.proxy_spider.proxy_spider.XiciSpider
#             # 获取 模块名和类名
#             module_name, class_name = full_class_name.rsplit(".", maxsplit=1)  # 根据右边的第一个"."进行截取,maxsplit=1表示截取一次
#             # print(full_class_name.rsplit(".", maxsplit=1))  # ['core.proxy_spider.proxy_spider', 'XiciSpider']
#             # print(module_name, class_name)
#
#             # 根据模块名 导入 模块, 动态导入模块
#             module = importlib.import_module(module_name)
#             # 根据类名,从模块中获取类
#             cls = getattr(module, class_name)
#             # 根据类,创建爬虫对象
#             spider = cls()
#             # print(spider)
#             yield spider
#
#     def run(self):
#         """1. 提供一个运行爬虫的run方法,作为运行爬虫的入口,实现核心的处理逻辑"""
#
#         # 2.1 根据配置文件信息,获取爬虫对象列表(即具体的爬虫类对象列表)
#         spiders = self.get_spider_from_settings()
#
#         # 2.2 遍历爬虫对象列表,获取爬虫对象,遍历爬虫对象的get_proxies方法,获取代理IP
#         for spider in spiders:
#             # 2.5 处理异常,防止一个爬虫内部出错,影响其他的爬虫
#             try:
#                 # 遍历爬虫对象的get_proxies方法,获取代理IP
#                 for proxy in spider.get_proxies():
#                     # print(type(proxy), proxy)
#
#                     # 2.3 检测代理IP(代理IP检测模块:httpbin_validator.py)
#                     proxy = check_proxy(proxy)
#
#                     # 2.4 如果IP可用,写入数据库(数据库模块: mongo_pool.py)
#                     # 如果protocol不等于-1,说明IP可用
#                     if proxy.protocol != -1:
#                         # 把可用IP写入到数据库
#                         self.mongo_pool.insert_one(proxy)
#             except Exception as e:
#                 # 爬虫报错,记录日志信息
#                 logger.exception(e)


if __name__ == '__main__':

    # 第一种 与 第二种方式
    # rs = RunSpider()
    # rs.run()

    # 第三种方式
    RunSpider.start()

    # 测试schedule
    # def task():
    #     print("测试schedule...")
    # schedule.every(2).seconds.do(task)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)


