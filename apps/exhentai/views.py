#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2020/10/25 
# CreatTIME : 1:45 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire

__author__ = 'RaXianch'

import sys
import json
import time
import random
from typing import Optional

# 响应数据构建器
from apps import constructResponse
from apps import logger
from apps.exhentai import app_name
from apps.exhentai import EXH_COOKIE
from apps.exhentai import router
from fastapi.responses import RedirectResponse
from fastapi.responses import FileResponse
from fastapi.responses import Response


@router.get("/")
async def exh():
    context = {
        "/search": "关键词搜索，get请求参数。q:str，搜索关键词,多个词使用+号分隔,组合词使用_代替空格,page:int,页码",
        "/id/{item_id}": "{item_id}:单本信息，int，漫画的id",
        "/thumb/{tid}": "{tid}:int，缩略图id",
    }
    return context


@router.get("/search")
async def exh_search(q: Optional[str] = "", page: Optional[int] = 1):
    """
    **exh_search** :

    - **name**: 漫画信息关键词搜索
    - **description**: url传参数,关键词搜索,使用get方式请求
    - **rely**: 依赖handlers.dbFormat.reglux,handlers.getWeb.base_load_web等方法
    - **param**[q]:  str，搜索关键词,多个词使用+号分隔，组合词使用_代替空格。默认值为a
    - **param**[page]:  int,页数。默认值为1
    - **return**: json,响应的数据咯~
    """
    # todo 无关搜索词时返回的数据处理
    from handlers.getWeb import base_load_web
    # 关键词切割，空格和空格的url转义字符都替换成+
    keyword = q.replace("+", "%20")
    tempDict = {
        "kw": q,
        "page": page,
        "pages": None,
        "results": None,
        "bookList": [],
    }
    callbackJson = constructResponse()
    headers = {
        "Cookie": random.choice(EXH_COOKIE)
    }
    param = {
        "page": page - 1 if page - 1 >= 0 else 0,
        "f_search": keyword,
    }
    # req = base_load_web(f"https://exhentai.org/?page={page - 1}&f_search={keyword}", headers=headers)
    req = base_load_web(f"https://exhentai.org/", params=param, headers=headers)
    # print(req.text)
    if req != None:
        from handlers.dbFormat import reglux
        import math
        from handlers.dbFormat import str_extract_num
        callbackJson.statusCode = req.status_code
        callbackJson.url = req.url

        # 获取搜索结果总数
        tempDict["results"] = int(str_extract_num("".join(reglux(req.text, r'Showing (.*?) results', False))))
        # 通过总数计算总页数
        tempDict["pages"] = int(math.ceil(tempDict["results"] / 25)) or 0
        bids = reglux(req.text, r'<a href="https://exhentai.org/g/([\s\S]*?)/([\s\S]*?)/">', False)
        names = reglux(req.text, r'class="glink">([\s\S]*?)</div>', False)
        thumbs = reglux(req.text, r'src="https://exhentai.org/t/.*?/.*?/([\s\S]*?).(jpg|png|jpeg|gif)"', False)
        # todo 星级等新字段添加
        for b, n, t in zip(bids, names, thumbs):
            print(b, n, t)
            tempItem = {
                "id": b[0],
                "hash": b[-1],
                "bname": n,
                "cover": "/ero/exh/t/{tname}.{bookImgSuffix}".format(tname=t[0], bookImgSuffix=t[1]),
                "url": "/ero/exh/id/%s/%s/" % (b[0], b[1]),
            }
            tempDict["bookList"].append(tempItem)
        if not tempDict["bookList"]:
            print(tempDict["bookList"])
            logger.warning(f"{app_name} {sys._getframe().f_code.co_name}")

    return callbackJson.callBacker(tempDict)


@router.get("/id/{item_id}/{hash_id}")
async def exh_item(item_id: int, hash_id: str, raw: Optional[bool] = False):
    """
    **exh_item** :

    - **name**: 漫画信息接口
    - **description**: 用对应id获取对应的本子漫画信息的接口,使用get方式请求
    - **rely**: 依赖handlers.dbFormat.reglux,handlers.getWeb.base_load_web等方法
    - **param**[item_id]:  int，漫画的id
    - **return**: json,响应的数据咯~
    """
    # todo 可能存在部分本子单页缺失问题
    from handlers.getWeb import base_load_web
    from handlers.dbFormat import str_2_encrypt
    baseDict = {
        "id": None,
        "hash": None,
        "origin": app_name,
        "title": None,
        "pages": None,
        "favorites": 0,
        "upload_date": None,
        "cover": None,
        "galleries": None,
        "tags": [],
        "raw": None,  # 原始数据
    }
    tempDict = baseDict.copy()
    callbackJson = constructResponse()
    # exh需要cookie
    headers = {
        "Cookie": random.choice(EXH_COOKIE)
    }
    req = base_load_web(f"https://exhentai.org/g/{item_id}/{hash_id}/", headers=headers)

    # 请求失败返回
    if req is None:
        return callbackJson.callBacker(tempDict)

    from handlers.dbFormat import reglux
    callbackJson.statusCode = req.status_code
    callbackJson.url = req.url

    # 获取本子图片总数
    tempDict["pages"] = int("".join(reglux(req.text, 'Length:</td><td class="gdt2">(.*?) pages</td></tr>', False)))

    # 获取本子图片格式后缀
    bookImgSuffix = "".join(reglux(
        req.text,
        r'background:transparent url\(https://exhentai.org/t/(.*?)\)',
        False))
    # # 生成封面地址
    tempDict["cover"] = "/ero/exh/t/{suffix}".format(
        suffix=bookImgSuffix)
    # 生成画廊地址
    tempDict["galleries"] = '/ero/exh/galleries/%s' % str_2_encrypt(
        f'{item_id}|{hash_id}|{tempDict["pages"]}'
    )

    # 是否提供原生数据
    if raw:
        tempDict["raw"] = [req.text]
    else:
        del tempDict["raw"]

    # 数据整理
    tempDict["id"] = item_id
    tempDict["hash"] = hash_id
    tempDict["title"] = {
        "full_name": "".join(reglux(req.text, "<title>(.*?) - ExHentai.org</title>", False)),
        "translated": "".join(reglux(req.text, '<h1 id="gj">(.*?)</h1>', False)),
        "abbre": "",
    }
    tempDict["favorites"] = int(
        "".join(reglux(req.text, 'id="favcount">(\d*?) times</td>', False)) or
        "".join(reglux(req.text, 'id="favcount">(.*?)</td>', False)).replace("Once", "1") or
        0
    )
    tempDict["tags"] = []
    tempDict["upload_date"] = "".join(reglux(req.text, 'Posted:</td><td class="gdt2">(.*?)</td>', False))
    return callbackJson.callBacker(tempDict)


@router.get("/galleries/{enc}")
async def exh_galleries(enc: str, raw: Optional[bool] = False):
    from handlers.getWeb import base_load_web
    from handlers.getWeb import thread_load_web
    from handlers.dbFormat import encrypt_2_str

    callbackJson = constructResponse()

    decStr = encrypt_2_str(enc).split("|")
    id = decStr[0] or None
    hash = decStr[1] or None
    pages = int(decStr[2]) or None
    baseDict = {
        "from": None,
        "pages": None,
        "thumbs": [],
        "images": [],
        "raw": None,
    }
    tempDict = baseDict.copy()
    callbackJson = constructResponse()
    # exh需要cookie
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Host": "exhentai.org",
        "Cookie": random.choice(EXH_COOKIE),
    }
    # req = base_load_web(f"https://exhentai.org/g/{id}/{hash}/?inline_set=ts_l", headers=headers)
    req = base_load_web(f"https://exhentai.org/g/{id}/{hash}/", headers=headers)

    # 请求失败返回
    if req is None:
        return callbackJson.callBacker(tempDict)

    import math
    from handlers.dbFormat import reglux
    callbackJson.statusCode = req.status_code
    callbackJson.url = req.url

    # 获取本子首页所有单页地址
    # exh html 不时出现变化，双路正则表达式
    thumbTemp = reglux(req.text, r'src="https://exhentai.org/t/[\s\S]{2}/[\s\S]{2}/([\s\S]*?)"', False) or []
    # 获取本子首页所有单页地址
    imagesTemp = []
    # exh html 不时出现变化，双路正则表达式
    imagesTemp += reglux(req.text, '<div class="gdtl" style="height:.*?px"><a href="(.*?)">', False) or \
                  reglux(req.text, 'no-repeat"><a href="(.*?)"><img alt', False)

    # 计算exh对本子的分页数
    gPages = math.ceil(pages / 20)
    # 大于1页才进行多页请求
    if gPages > 1:
        # 生成exh本子分页地址列表
        gUrlPagesUrl = []
        for i in range(1, gPages):
            gUrlPagesUrl.append(f"https://exhentai.org/g/{id}/{hash}/?p={i}")

        #  对本子分页发出请求，获取各个分页中所有单页地址并合并到返回数据中
        subPages = thread_load_web(gUrlPagesUrl, headers=headers, inspectStr="IP address has been temporarily banned")
        print(subPages)
        for k, v in subPages.items():
            if v is None:
                continue
            itemp = reglux(v.text, '<div class="gdtl" style="height:.*?px"><a href="(.*?)">', False) or \
                   reglux(v.text, 'no-repeat"><a href="(.*?)"><img alt', False) or []
            tTemp = reglux(v.text, r'src="https://exhentai.org/t/[\s\S]{2}/[\s\S]{2}/([\s\S]*?)"', False) or []
            print(f"{v.url}|{len(list(set(tTemp)))}|{len(list(set(tTemp)))}")
            if len(tTemp) == 0:
                print(v.text)
            thumbTemp += tTemp
            imagesTemp += itemp

    # 数据整理
    tempDict["thumbs"] = list(set([f"/ero/exh/t/{i}" for i in thumbTemp]))
    tempDict["images"] = list(map(lambda x: f"/ero/exh/i/{x.split('/s/')[-1]}/", imagesTemp))
    return callbackJson.callBacker(tempDict)


@router.get("/i/{book_hash}/{picture_id}/")
async def exh_images(book_hash: str, picture_id: str, ):
    from handlers.getWeb import base_load_web
    from handlers.dbFormat import reglux
    headers = {
        "Cookie": random.choice(EXH_COOKIE)
    }
    url = f"https://exhentai.org/s/{book_hash}/{picture_id}"
    req = base_load_web(url, headers=headers)
    # 请求失败返回
    if req is None:
        return Response(status_code=404)

    imgUrl = "".join(reglux(req.text, '<img id="img" src="(.*?)"', False))
    r = base_load_web(imgUrl, headers=headers)
    return Response(content=r.content)


@router.get("/t/{tname}")
async def exh_thumb(tname: str):
    # todo 处理方式还不够完美
    if len(tname) < 8:
        return Response(status_code=404)
    from handlers.getWeb import base_load_web
    headers = {
        "Cookie": random.choice(EXH_COOKIE)
    }
    url = "https://exhentai.org/t/" + tname[0] + tname[1] + "/" + tname[2] + tname[3] + "/" + tname
    r = base_load_web(url, headers=headers)
    return Response(content=r.content)

# todo 单页列表分离

# todo exh ban ip
# Your IP address has been temporarily banned for excessive pageloads which indicates that you are using automated mirroring/harvesting software. The ban expires in 48 minutes and 16 seconds
