#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2020/10/23 
# CreatTIME : 15:57 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire

__author__ = 'RaXianch'

import time
from server import RES_CALLBACK


class constructResponse(object):
    """
    统一响应构建器

    settings文件中的CUSTO_CALLBACK_DATA在这里也将会整合
    各apps的views响应的数据也会统一放置到BASE_CALLBACK_DATA的data字段里
    自动计算请求耗时，响应时间，时间戳，以及响应码和响应信息
    """
    def __init__(self):
        self.startTime = time.time()
        self.endTime = None
        self.resData = RES_CALLBACK.copy()
        self.statusCode = 404

    def callBacker(self, data=None):
        if data is None:
            data = {}

        self.resData["status_code"] = self.statusCode
        if 200 <= self.statusCode < 300:
            self.resData["status_bool"] = True
            self.resData["message"] = "OK!"
        else:
            self.resData["message"] = "数据拉取时发生错误！"

        if data:
            self.endTime = time.time()
            self.resData["cost_time"] = "%s 秒" % round(self.endTime - self.startTime, 2)
            self.resData["data"] = data

        self.resData["ts"] = self.endTime
        self.resData["date"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return self.resData

# todo 自定义错误响应