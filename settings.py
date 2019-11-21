# -*- coding:utf-8 -*-
# @Desc : 
# @Author : Administrator
# @Date : 2019-11-18 10:27


import logging


# 在配置文件: settings.py 中定义MAX_SCORE = 50,表示代理IP的默认最高分值
MAX_SCORE = 50

# 日志的配置信息
LOG_LEVEL = logging.DEBUG  # INFO默认等级
LOG_MFT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s'  # 默认日志格式
LOG_DATEMFT = '%Y-%m-%d %H:%M:%S'  # 默认时间格式
LOG_FILENAME = 'log.log'  # 默认日志文件名称

# 测试代理IP超时时间
TEST_TIMEOUT = 10

# 配置MongoDB数据库
MONGO_URL = "mongodb://127.0.0.1:27017"

# 获取爬虫对象列表(即具体的爬虫类对象列表)
PROXIES_SPIDERS = [
    # 具体爬虫的全类名,路径: 模块.类名
    "core.proxy_spider.proxy_spider.XiciSpider",
    "core.proxy_spider.proxy_spider.KuaidailiSpider",
    "core.proxy_spider.proxy_spider.Ip66Spider",
    "core.proxy_spider.proxy_spider.Ip3366Spider",
]

# 修改配置文件,增加爬虫运行时间间隔的配置,单位为小时
RUN_SPIDRS_INTERVAL = 12