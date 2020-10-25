#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2020/10/23 
# CreatTIME : 12:56 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire

__author__ = 'RaXianch'

from typing import Optional

from fastapi import FastAPI
from apps.routers import api_router
from fastapi import APIRouter
import time


app = FastAPI()
app.include_router(api_router, prefix="/ero")


@app.get("/")
async def index():
    context = {
        "TIME": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "/nh": "nh来源，试做",
        "/eh": "eh来源，还未完成",
        "/exh": "exh来源，还未完成",
        "todo": "各种处理器（上传、各类检查和验证器、数据清洗格式化、异步数据库操作、爬虫）、应用分级路由及其视图开发和设计、docs验证、设置文件的完善、docker封装"
    }
    return context

@app.get("/ero")
async def index():
    context = {
        "TIME": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
    }
    print(context)
    return context

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}