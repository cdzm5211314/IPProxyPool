# -*- coding:utf-8 -*-
# @Desc : 
# @Author : Administrator
# @Date : 2019-11-18 10:25


from settings import MAX_SCORE


class Proxy(object):

    def __init__(self, ip, port, protocol=-1, score=MAX_SCORE, disable_domains=[]):
    # def __init__(self, ip, port, protocol=-1, nick_type=-1, speed=-1, area=None, score=MAX_SCORE, disable_domains=[]):
        self.ip = ip  # 代理IP地址
        self.port = port  # 代理IP端口号
        self.protocol = protocol  # 代理IP支持的协议: http 0, https 1, http&https 2
        # self.nick_type = nick_type  # 代理IP的匿名程度: 高匿 0, 匿名 1, 透明 2
        # self.speed = speed  # 代理IP的响应速度,秒s
        # self.area = area  # 代理IP所在地区
        self.score = score  # 代理IP的评分,用于衡量代理的可用性
        # # 默认分值可以通过配置文件进行设置,在进行代理IP可用性检查的时候,每遇到一次请求失败就减1分,减到0的时候就从池中删除
        self.disable_domains = disable_domains  # 不可用域名列表,有些代理IP在某些域名下不可用,而在一些于明霞可用

    def __str__(self):

        return str(self.__dict__)



