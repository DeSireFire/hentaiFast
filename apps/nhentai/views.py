#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2020/10/25 
# CreatTIME : 1:45 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire

__author__ = 'RaXianch'

import json
import random
from typing import Optional

# 响应数据构建器
from apps import constructResponse
from apps.nhentai import app_name
from apps.nhentai import router
from fastapi.responses import RedirectResponse
from fastapi.responses import FileResponse
from fastapi.responses import Response


# 视图函数
@router.get("/")
async def nh():
    context = {
        "/random": "随机本子，状态码300+",
        "/search": "关键词搜索，get请求参数。q:str，搜索关键词,多个词使用+号分隔,组合词使用_代替空格,page:int,页码",
        "/id/{item_id}": "{item_id}:单本信息，int，漫画的id",
        "/galleries/{hash}/{page}": "{hash}:str，本子hash,page:int,页码",
        "/thumb/{tid}": "{tid}:int，缩略图id",
    }
    return context


@router.get("/random")
async def nh_random():
    """
    **nh_random** :

    - **name**: 随机漫画接口
    - **description**: 使用get方式请求,跳转到随机idd的本子数据
    - **return**: json,响应的数据咯~
    """
    bid = random.randint(1, 300000)
    return RedirectResponse("/ero/nh/id/%s" % bid)


@router.get("/search")
async def nh_search(q: Optional[str] = "a", page: Optional[int] = 1):
    """
    **nh_search** :

    - **name**: 漫画信息关键词搜索
    - **description**: url传参数,关键词搜索,使用get方式请求
    - **rely**: 依赖handlers.dbFormat.reglux,handlers.getWeb.base_load_web等方法
    - **param**[q]:  str，搜索关键词,多个词使用+号分隔，组合词使用_代替空格。默认值为a
    - **param**[page]:  int,页数。默认值为1
    - **return**: json,响应的数据咯~
    """
    #todo 无关搜索词时返回的数据处理
    from handlers.getWeb import base_load_web
    # 关键词切割，空格和空格的url转义字符都替换成+
    keyword = q.replace(" ", "+").replace("%20", "+")
    tempDict = {
        "kw": q,
        "page": page,
        "pages": None,
        "results": None,
        "bookList": [],
    }
    callbackJson = constructResponse()
    req = base_load_web("https://nhentai.net/search/?q=%s" % keyword)
    if req != None:
        from handlers.dbFormat import reglux
        from handlers.dbFormat import str_extract_num
        callbackJson.statusCode = req.status_code
        tempDict["pages"] = "".join(
            reglux(req.text, r'<a href="/search/\?q=.*?\&amp\;page=(\d*?)" class="last">', False))
        bids = reglux(req.text, r'<ahref="/g/(\d*?)/"class="cover"style="padding', True)
        names = reglux(req.text, r'<div class="caption">(.*?)</div>', False)
        thumbs = reglux(req.text, r'<noscript><img src="([\s\S]*?)"', False)
        for b, n, t in zip(bids, names, thumbs):
            tempItem = {
                "id": b,
                "hash": str_extract_num(t),
                "bname": n,
                "cover": "/ero/nh/t/{tid}/thumb.{tname}".format(
                    tid=str_extract_num(t), tname="png" if "png" in t else "jpg"),
                "url": "/ero/nh/id/%s/" % b,
            }
            tempDict["bookList"].append(tempItem)
        tempDict["results"] = len(tempDict["bookList"])
    return callbackJson.callBacker(tempDict)


@router.get("/id/{item_id}")
async def nh_item(item_id: int, raw: Optional[bool] = False):
    """
    **nh_item** :

    - **name**: 漫画信息接口
    - **description**: 用对应id获取对应的本子漫画信息的接口,使用get方式请求
    - **rely**: 依赖handlers.dbFormat.reglux,handlers.getWeb.base_load_web等方法
    - **param**[item_id]:  int，漫画的id
    - **return**: json,响应的数据咯~
    """
    from handlers.getWeb import base_load_web
    from handlers.dbFormat import str_2_encrypt
    tempStr = "{}"
    tempDict = {
        "id": None,
        "hash": None,
        "origin": app_name,
        "title": None,
        "pages": None,
        "favorites": None,
        "upload_date": None,
        "cover": None,
        "galleries": None,
        "tags": [],
        "raw": None,    # 原始数据
    }
    callbackJson = constructResponse()
    req = base_load_web("https://nhentai.net/g/%s/" % item_id)
    # 请求失败返回
    if req is None:
        return callbackJson.callBacker(tempDict)

    from handlers.dbFormat import reglux
    callbackJson.statusCode = req.status_code
    tempStr = "".join(reglux(req.text, r'window._gallery = JSON.parse\("([\s\S]*?)"\);', False)).encode(
        "utf-8").decode('unicode-escape')
    rawData = json.loads(tempStr)
    tempDict["id"] = rawData["id"]
    tempDict["hash"] = rawData["media_id"]
    tempDict["title"] = {
        "full_name": rawData["title"]["english"],
        "translated": rawData["title"]["japanese"],
        "abbre": rawData["title"]["pretty"],
    }
    tempDict["favorites"] = rawData["num_favorites"]
    tempDict["pages"] = rawData["num_pages"]
    tempDict["tags"] = rawData["tags"]
    tempDict["upload_date"] = rawData["upload_date"]

    # 获取本子图片格式后缀
    bookImgSuffix = "".join(reglux(req.text, r'data-src="https://t.nhentai.net/galleries/\d*/cover.(jpg|png)"', False))
    # 生成封面地址
    tempDict["cover"] = "/ero/nh/t/{cid}/cover.{suffix}".format(
        cid=rawData["media_id"],
        suffix=bookImgSuffix)
    # 生成画廊地址
    tempDict["galleries"] = '/ero/nh/galleries/%s' % str_2_encrypt(
        f'{rawData["id"]}|{rawData["media_id"]}|{rawData["num_pages"]}'
    )
    # 是否提供原生数据
    if raw:
        tempDict["raw"] = rawData
    else:
        del tempDict["raw"]

    return callbackJson.callBacker(tempDict)


@router.get("/galleries/{enc}")
async def nh_galleries(enc: str, raw: Optional[bool] = False):
    """
    **nh_item** :

    - **name**: 漫画信息接口
    - **description**: 用对应id获取对应的本子漫画信息的接口,使用get方式请求
    - **rely**: 依赖handlers.dbFormat.reglux,handlers.getWeb.base_load_web等方法
    - **param**[item_id]:  int，漫画的id
    - **return**: json,响应的数据咯~
    """
    from handlers.getWeb import base_load_web
    from handlers.dbFormat import encrypt_2_str

    callbackJson = constructResponse()

    decStr = encrypt_2_str(enc).split("|")
    id = decStr[0] or None
    hash = decStr[1] or None
    pages = decStr[2] or None
    tempDict = {
        "from": None,
        "pages": None,
        "thumbs": [],
        "images": [],
        "raw": None,
    }
    req = base_load_web("https://nhentai.net/g/%s/" % id)
    # 请求失败返回
    if req is None:
        return callbackJson.callBacker(tempDict)
    from handlers.dbFormat import reglux
    callbackJson.statusCode = req.status_code
    tempT = reglux(req.text, r'data-src="https://t.nhentai.net/galleries/\d*/(\d*)t.(jpg|png)"', False)

    # 是否提供原生数据
    if id and hash and pages:
        tempDict["from"] = f'/ero/nh/id/{id}'
        tempDict["pages"] = int(pages)
        tempDict["thumbs"] = [f"/ero/nh/t/{hash}/{i[0]}t.{i[1]}" for i in tempT]
        tempDict["images"] = [f"/ero/nh/i/{hash}/{i[0]}.{i[1]}" for i in tempT]

    # 是否提供原生数据
    if raw:
        tempDict["raw"] = req.text
    else:
        del tempDict["raw"]

    return callbackJson.callBacker(tempDict)


@router.get("/i/{mid}/{iname}")
async def nh_images(mid: int, iname: str):
    from handlers.getWeb import base_load_web
    url = f"https://i.nhentai.net/galleries/{mid}/{iname}"
    r = base_load_web(url)
    return Response(content=r.content)


@router.get("/t/{tid}/{tname}")
async def nh_thumb(tid: int, tname: str):
    from handlers.getWeb import base_load_web
    url = f'https://t.nhentai.net/galleries/{tid}/{tname}'
    r = base_load_web(url)
    return Response(content=r.content or {})
