#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2020/10/23 
# CreatTIME : 12:53 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire

__author__ = 'RaXianch'

"""
网络请求器
"""
from requests.adapters import HTTPAdapter
import requests
import sys
import os
import asyncio
import nest_asyncio
nest_asyncio.apply()

try:
    from server import *

except ModuleNotFoundError as e:
    # 解决终端直接运行main.py找不到项目自建模块的问题
    sys.path.append(os.path.dirname(sys.path[0]))

    from server import *



def base_load_web(url, headers=None, timeout=TIMEOUT, reTry=RETRY_MAX, verify=VERIFY):
    # 请求初始化
    s = requests.Session()
    # 首次代理设置和重试时代理设置
    proxiesList = [{}, {}]
    # 减去首次重试次数
    reTry -= 1
    # 返回值
    # callBack = {"status": False, "response": None, "Exception": ""}
    callBack = None
    # 检查使用请求头
    if headers:
        s.headers = headers
    else:
        s.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
            'Accept-Encoding': 'gzip, deflate',
            'Accept': '*/*',
            "referer": url,
            'Connection': 'keep-alive'
        }

    # 代理设置检查
    if ONPROXY:
        # 代理设置不为空，重试代理设置值存在，且其值为真时全局使用代理请求
        if PROXY_SETTING and PROXY_SETTING.get("reTryProxy", False) is True:
            proxiesList[0] = PROXY_SETTING
            proxiesList[1] = PROXY_SETTING
        # 代理设置不为空，重试代理设置值存在，且其值为假时第一次链接超时才开始使用代理
        elif PROXY_SETTING and PROXY_SETTING.get("reTryProxy", False) is False:
            proxiesList[1] = PROXY_SETTING

    # 重试次数设置
    try:
        s.proxies = proxiesList[0]
        r = s.get(url, timeout=timeout, verify=verify)
        callBack = r
        # callBack["status"] = True
        # callBack["response"] = r
    except requests.exceptions.RequestException as e:
        print("触发超时重试 %s" % e)
        # 超时重试
        s.mount('http://', HTTPAdapter(max_retries=reTry))
        s.mount('https://', HTTPAdapter(max_retries=reTry))
        s.proxies = proxiesList[1]
        r = s.get(url, timeout=timeout, verify=verify)
        # callBack["status"] = True
        # callBack["response"] = r
        callBack = r

    # 全局抓取错误
    except Exception as allE:
        print(allE)
    finally:
        return callBack


if __name__ == '__main__':
    # 测试代码
    demo = base_load_web('https://nhentai.net/g/249664/')
    if demo != None:
        from handlers.dbFormat import reglux
        import json
        # print(demo.content.decode(encoding="utf-8", errors='unicode-escape'))
        tempStr = "".join(reglux(demo.text, r'window._gallery = JSON.parse\("([\s\S]*?)"\);', False)).encode("utf-8").decode('unicode-escape')
        print(tempStr)
        print(json.loads(tempStr))
        # print(json.loads(tempStr))
