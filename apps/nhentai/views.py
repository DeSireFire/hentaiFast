#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2020/10/25 
# CreatTIME : 1:45 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire

__author__ = 'RaXianch'

import json
from typing import Optional

# 响应数据构建器
from apps import constructResponse
from apps.nhentai import app_name
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from fastapi.responses import FileResponse

# 声明视图子路由
router = APIRouter()


# 视图函数
@router.get("/")
async def nh():
    return {}


@router.get("/random")
async def nh_random():
    from handlers.getWeb import base_load_web
    return {}


@router.get("/search")
async def nh_search(q: Optional[str] = None, page: Optional[int] = 1):
    from handlers.getWeb import base_load_web
    # 关键词切割，空格和空格的url转义字符都替换成+
    keyword = q.replace(" ", "+").replace("%20", "+")
    tempDict = {
        "kw": q,
        "page": page,
        "pages": None,
        "bookList": [],
    }
    callbackJson = constructResponse()
    req = base_load_web("https://nhentai.net/search/?q=%s" % keyword)
    if req != None:
        from handlers.dbFormat import reglux
        callbackJson.statusCode = req.status_code
        tempDict["pages"] = "".join(
            reglux(req.text, r'<a href="/search/\?q=.*?\&amp\;page=(\d*?)" class="last">', False))
        bids = reglux(req.text, r'<ahref="/g/(\d*?)/"class="cover"style="padding', True)
        names = reglux(req.text, r'<div class="caption">(.*?)</div>', False)
        thumbs = reglux(req.text, r'<noscript><img src="([\s\S]*?)"', False)
        for b, n, t in zip(bids, names, thumbs):
            tempItem = {
                "id": b,
                "bname": n,
                "cover": t,
                # "url": "https://nhentai.net/g/%s/" % b,
                "url": "/ero/nh/id/%s/" % b,
            }
            tempDict["bookList"].append(tempItem)
    return callbackJson.callBacker(tempDict)


@router.get("/id/{item_id}")
async def nh_item(item_id: int):
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
        "origin": app_name,
        "id": None,
        "title": None,
        "pages": None,
        "favorites": None,
        "upload_date": None,
        "images": [],
        "tags": [],
        "raw": None,    # 原始数据
    }
    callbackJson = constructResponse()
    req = base_load_web("https://nhentai.net/g/%s/" % item_id)
    if req is not None:
        # todo 数据结构统一
        from handlers.dbFormat import reglux
        callbackJson.statusCode = req.status_code
        tempStr = "".join(reglux(req.text, r'window._gallery = JSON.parse\("([\s\S]*?)"\);', False)).encode(
            "utf-8").decode('unicode-escape')
    return callbackJson.callBacker(json.loads(tempStr))


