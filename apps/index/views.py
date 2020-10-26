#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2020/10/26 
# CreatTIME : 20:17 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire

__author__ = 'RaXianch'
import time
from fastapi import APIRouter
router = APIRouter()

@router.get("/")
async def index():
    context = {
        "TIME": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "/nh": "nh来源，试做",
        "/eh": "eh来源，还未完成",
        "/exh": "exh来源，还未完成",
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