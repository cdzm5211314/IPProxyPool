# -*- coding:utf-8 -*-
# @Desc : 代理池的检测模块
# @Author : Administrator
# @Date : 2019-11-18 10:24

# 目的: 检测代理IP的可用性,保证代理池中的IP基本可用

from settings import MAX_SCORE
from core.db.mongo_pool import MongoPool
from core.proxy_validate.httpbin_validator import check_proxy


# 第一种方式: 提供run方法,用于处理检测代理IP可用性的核心逻辑
class ProxyTester(object):

    def __init__(self):
        # 创建操作数据库的MongoPool对象
        self.mongo_pool = MongoPool()

    def run(self):
        """提供run方法,用于处理检测代理IP可用性的核心逻辑"""
        # 2.1 从数据库中获取所有的代理IP
        proxies = self.mongo_pool.find_all()
        # 2.2 遍历代理IP列表
        for proxy in proxies:
            # 2.3 检查代理IP可用性
            proxy = check_proxy(proxy)
            # 2.4 如果代理IP不可用, 就让代理IP分值减一, 如果代理IP分值等于0就从数据库中删除该代理IP, 否则就更新该代理IP
            if proxy.protocol == -1:
                proxy.score -= 1  # 代理IP减一
                if proxy.score ==0:  #如果代理IP分值等于0
                    # 从数据库中删除该代理IP
                    self.mongo_pool.delete_one(proxy)
                else:
                    # 否则就更新该代理IP
                    self.mongo_pool.update_one(proxy)
            else:
                # 2.5 如果代理IP可用, 就让代理IP分值恢复, 并且更新到数据库中
                proxy.score = MAX_SCORE
                self.mongo_pool.update_one(proxy)



if __name__ == '__main__':

    tester = ProxyTester()
    tester.run()



