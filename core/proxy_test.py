# -*- coding:utf-8 -*-
# @Desc : 代理池的检测模块
# @Author : Administrator
# @Date : 2019-11-18 10:24

# 目的: 检测代理IP的可用性,保证代理池中的IP基本可用

from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
from queue import Queue

from settings import MAX_SCORE, TEST_PROXIES_ASYNC_COUNT
from core.db.mongo_pool import MongoPool
from core.proxy_validate.httpbin_validator import check_proxy


# 第二种方式: 提高检测速度,使用异步方式执行检测任务
class ProxyTester(object):

    def __init__(self):
        # 创建操作数据库的MongoPool对象
        self.mongo_pool = MongoPool()
        # 3.1 在init方法中创建队列和协程池
        self.queue = Queue()
        self.coroutine_pool = Pool()

    # 回调函数
    def __check_callback(self, temp):
        self.coroutine_pool.apply_async(self.__check_one_proxy, callback=self.__check_callback)

    def run(self):
        """提供run方法,用于处理检测代理IP可用性的核心逻辑"""
        # 2.1 从数据库中获取所有的代理IP
        proxies = self.mongo_pool.find_all()
        # 2.2 遍历代理IP列表
        for proxy in proxies:
            # 3.2 把要检测的代理IP,放到队列中
            self.queue.put(proxy)

        # 3.5 开启多个异步任务,来处理代理IP的检测,可以通过配置文件指定异步数量
        for i in range(TEST_PROXIES_ASYNC_COUNT):
            # 3.4 通过异步回调,使用死循环不断执行这个方法
            self.coroutine_pool.apply_async(self.__check_one_proxy, callback=self.__check_callback)

        # 让当前线程,等待队列任务的完成
        self.queue.join()

    def __check_one_proxy(self):
        """检测一个代理IP的可用性"""
        # 3.3 把要检测一个代理IP的可用性代码抽取到一个方法中;从队列中获取代理IP,进行检测,检测完毕;调度队列的task_done方法
        proxy = self.queue.get()
        # 2.3 检查代理IP可用性
        proxy = check_proxy(proxy)
        # 2.4 如果代理IP不可用, 就让代理IP分值减一, 如果代理IP分值等于0就从数据库中删除该代理IP, 否则就更新该代理IP
        if proxy.protocol == -1:
            proxy.score -= 1  # 代理IP减一
            if proxy.score == 0:  # 如果代理IP分值等于0
                # 从数据库中删除该代理IP
                self.mongo_pool.delete_one(proxy)
            else:
                # 否则就更新该代理IP
                self.mongo_pool.update_one(proxy)
        else:
            # 2.5 如果代理IP可用, 就让代理IP分值恢复, 并且更新到数据库中
            proxy.score = MAX_SCORE
            self.mongo_pool.update_one(proxy)

        # 调度队列的task_done方法
        self.queue.task_done()

# 第一种方式: 提供run方法,用于处理检测代理IP可用性的核心逻辑
# class ProxyTester(object):
#
#     def __init__(self):
#         # 创建操作数据库的MongoPool对象
#         self.mongo_pool = MongoPool()
#
#     def run(self):
#         """提供run方法,用于处理检测代理IP可用性的核心逻辑"""
#         # 2.1 从数据库中获取所有的代理IP
#         proxies = self.mongo_pool.find_all()
#         # 2.2 遍历代理IP列表
#         for proxy in proxies:
#             # 2.3 检查代理IP可用性
#             proxy = check_proxy(proxy)
#             # 2.4 如果代理IP不可用, 就让代理IP分值减一, 如果代理IP分值等于0就从数据库中删除该代理IP, 否则就更新该代理IP
#             if proxy.protocol == -1:
#                 proxy.score -= 1  # 代理IP减一
#                 if proxy.score ==0:  #如果代理IP分值等于0
#                     # 从数据库中删除该代理IP
#                     self.mongo_pool.delete_one(proxy)
#                 else:
#                     # 否则就更新该代理IP
#                     self.mongo_pool.update_one(proxy)
#             else:
#                 # 2.5 如果代理IP可用, 就让代理IP分值恢复, 并且更新到数据库中
#                 proxy.score = MAX_SCORE
#                 self.mongo_pool.update_one(proxy)



if __name__ == '__main__':

    tester = ProxyTester()
    tester.run()



