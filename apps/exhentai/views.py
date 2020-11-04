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
    from handlers.getWeb import base_load_web, thread_load_web
    tempDict = {
        "id": None,
        "hash": None,
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
    headers = {
        "Cookie": random.choice(EXH_COOKIE)
    }
    req = base_load_web(f"https://exhentai.org/g/{item_id}/{hash_id}/", headers=headers)

    if req is not None:
        import math
        from handlers.dbFormat import reglux
        callbackJson.statusCode = req.status_code

        # 获取本子图片总数
        tempDict["pages"] = int("".join(reglux(req.text, 'Length:</td><td class="gdt2">(.*?) pages</td></tr>', False)))
        # 获取本子首页所有单页地址
        tempDict["images"] += reglux(req.text, '<div class="gdtl" style="height:320px"><a href="(.*?)">', False)

        # 生成exh本子分页地址列表
        gPages = []
        for i in range(1, math.ceil(tempDict["pages"]/20)+1):
            gPages.append(f"https://exhentai.org/g/{item_id}/{hash_id}/?p={i}")

        #  对本子分页发出请求，获取各个分页中所有单页地址并合并到返回数据中
        subPages = thread_load_web(gPages, headers=headers)
        for k, v in subPages.items():
            tempDict["images"] += reglux(v.text, '<div class="gdtl" style="height:320px"><a href="(.*?)">', False)

        tempDict["id"] = item_id
        tempDict["hash"] = hash_id
        tempDict["title"] = {
            "full_name": "".join(reglux(req.text, "<title>(.*?) - ExHentai.org</title>", False)),
            "translated": "".join(reglux(req.text, '<h1 id="gj">(.*?)</h1>', False)),
            "abbre": "",
        }
        tempDict["favorites"] = "".join(reglux(req.text, '<td class="gdt2" id="favcount">(.*?) times</td>', False))
        tempDict["tags"] = []
        tempDict["upload_date"] = "".join(reglux(req.text, 'Posted:</td><td class="gdt2">(.*?)</td>', False))
        tempDict["raw"] = [req.text]
    return callbackJson.callBacker(tempDict)
