# -*- coding:utf-8 -*-
# @Desc : 代理池的启动入口
# @Author : Administrator
# @Date : 2019-11-18 10:26

# 目的: 把 启动爬虫,启动检测代理IP,启动Flask的WEB服务 统一到一起
# 思路: 开启三个进程,分别用于启动 爬虫,检测代理IP,WEB服务

from multiprocessing import Process
from core.proxy_spider.run_spider import RunSpider
from core.proxy_test import ProxyTester
from core.proxy_api import ProxyApi

# 1. 定义一个run方法,用于启动代理池
def run():

    # 1.1 定义一个列表,用于存储要启动的进程
    process_list = []

    # 1.2 创建 启动爬虫 的进程,添加到列表中
    process_list.append(Process(target=RunSpider.start))
    # 1.3 创建 启动检测代理IP 的进程,添加到列表中
    process_list.append(Process(target=ProxyTester.start))
    # 1.4 创建 启动提供API服务 的进程,添加到列表中
    process_list.append(Process(target=ProxyApi.start))

    # 1.5 遍历进程列表,启动所有的进程
    for process in process_list:
        process.daemon = True  # 设置守护进程
        process.start()  # 开启进程

    # 1.6 遍历进程列表,让主进程等待子进程的完成
    for process in process_list:
        process.join()


# 2. 在 if __name__ == "__main__" 中调用run方法
if __name__ == "__main__":

    run()


