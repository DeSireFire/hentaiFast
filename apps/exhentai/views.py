#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2020/10/25 
# CreatTIME : 1:45 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire

__author__ = 'RaXianch'
import json
import time
import random
from typing import Optional

# 响应数据构建器
from apps import constructResponse
from apps.exhentai import app_name
from apps.exhentai import EXH_COOKIE
from apps.exhentai import router
from fastapi.responses import RedirectResponse
from fastapi.responses import FileResponse
from fastapi.responses import Response


@router.get("/")
async def nh():
    from handlers.getWeb import base_load_web
    tempStr = "{}"
    start_time = time.time()
    req = base_load_web("https://nhentai.net/g/249664/")
    if req != None:
        from handlers.dbFormat import reglux
        tempStr = "".join(reglux(req.text, r'window._gallery = JSON.parse\("([\s\S]*?)"\);', False)).encode("utf-8").decode('unicode-escape')
    end_time = time.time()
    return {"costTime": end_time-start_time, "content": json.loads(tempStr)}


@router.get("/id/{item_id}/{hash_id}")
async def exh_item(item_id: int, hash_id: str):
    """
    **nh_item** :

    - **name**: 漫画信息接口
    - **description**: 用对应id获取对应的本子漫画信息的接口,使用get方式请求
    - **rely**: 依赖handlers.dbFormat.reglux,handlers.getWeb.base_load_web等方法
    - **param**[item_id]:  int，漫画的id
    - **return**: json,响应的数据咯~
    """
    from handlers.getWeb import base_load_web
    tempStr = "{}"
    tempDict = {
        "id": None,
        "origin": app_name,
        "title": None,
        "pages": None,
        "favorites": None,
        "upload_date": None,
        "images": [],
        "tags": [],
        "raw": None,    # 原始数据
    }
    callbackJson = constructResponse()
    print(app_name)
    headers = {
        "Cookie": random.choice(EXH_COOKIE)
    }
    req = base_load_web(f"https://exhentai.org/g/{item_id}/{hash_id}/", headers=headers)

    if req is not None:
        from handlers.dbFormat import reglux
        callbackJson.statusCode = req.status_code
        # tempStr = "".join(reglux(req.text, r'window._gallery = JSON.parse\("([\s\S]*?)"\);', False)).encode(
        #     "utf-8").decode('unicode-escape')
        print(req)
        # rawData = json.loads(tempStr)
        # tempDict["raw"] = rawData
        # tempDict["id"] = rawData["id"]
        # tempDict["title"] = {
        #     "full_name": rawData["title"]["english"],
        #     "translated": rawData["title"]["japanese"],
        #     "abbre": rawData["title"]["pretty"],
        # }
        # tempDict["favorites"] = rawData["num_favorites"]
        # tempDict["pages"] = rawData["num_pages"]
        # tempDict["tags"] = rawData["tags"]
        # tempDict["upload_date"] = rawData["upload_date"]

    return callbackJson.callBacker(tempDict)
