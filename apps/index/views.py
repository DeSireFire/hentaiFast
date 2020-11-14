#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2020/10/26 
# CreatTIME : 20:17 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire

__author__ = 'RaXianch'
import time
import json
from apps.exhentai import router

@router.get("/")
async def index():
    context = {
        "TIME": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "/ero": {
            "/nh": "nh模块",
            "/exh": "exh模块",
            "/eh": "eh来源，还未完成",
        },
        "todo": "各种处理器（上传、各类检查和验证器、数据清洗格式化、异步数据库操作、爬虫）、应用分级路由及其视图开发和设计、docs验证、设置文件的完善、docker封装"
    }
    return context


@router.get("/reload")
async def index():
    from config.settings import BASE_DIR
    import os
    with open(os.path.join(BASE_DIR, "runServer.py"), 'a+') as f:
        f.write("\n    print(%s)" % time.time())
    return {}


@router.get("/demo")
async def exh():
    from handlers.getWeb import base_load_web
    tempStr = "{}"
    start_time = time.time()
    req = base_load_web("https://nhentai.net/g/249664/")
    if req != None:
        from handlers.dbFormat import reglux
        tempStr = "".join(reglux(req.text, r'window._gallery = JSON.parse\("([\s\S]*?)"\);', False)).encode("utf-8").decode('unicode-escape')
    end_time = time.time()
    return {"costTime": end_time-start_time, "content": json.loads(tempStr)}
