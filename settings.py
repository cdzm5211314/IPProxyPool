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


