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
    #todo 无关搜索词时返回的数据处理
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
    req = base_load_web(f"https://exhentai.org/?page={page-1}&f_search={keyword}", headers=headers)
    if req != None:
        from handlers.dbFormat import reglux
        import math
        from handlers.dbFormat import str_extract_num
        callbackJson.statusCode = req.status_code
        # 获取搜索结果总数
        tempDict["results"] = int(str_extract_num("".join(reglux(req.text, r'Showing (.*?) results', False))))
        # 通过总数计算总页数
        tempDict["pages"] = math.ceil(tempDict["results"]/25)
        bids = reglux(req.text, r'<a href="https://exhentai.org/g/([\s\S]*?)/">', False)
        names = reglux(req.text, r'class="glink">([\s\S]*?)</div>', False)
        thumbs = reglux(req.text, r'src="https://exhentai.org/t/.*?/.*?/([\s\S]*?).jpg"', False)
        # todo id&hash是否分离。星级等新字段添加
        for b, n, t in zip(bids, names, thumbs):
            tempItem = {
                "id": b,
                "bname": n,
                "cover": "/ero/exh/thumb/%s/" % t,
                "url": "/ero/exh/id/%s/" % b,
            }
            tempDict["bookList"].append(tempItem)
    return callbackJson.callBacker(tempDict)

@router.get("/id/{item_id}/{hash_id}")
async def exh_item(item_id: int, hash_id: str):
    """
    **exh_item** :

    - **name**: 漫画信息接口
    - **description**: 用对应id获取对应的本子漫画信息的接口,使用get方式请求
    - **rely**: 依赖handlers.dbFormat.reglux,handlers.getWeb.base_load_web等方法
    - **param**[item_id]:  int，漫画的id
    - **return**: json,响应的数据咯~
    """
    # todo 可能存在部分本子单页缺失问题
    from handlers.getWeb import base_load_web, thread_load_web
    baseDict = {
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
    tempDict = baseDict.copy()
    callbackJson = constructResponse()
    # exh需要cookie
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
        imagesTemp = []
        imagesTemp += reglux(req.text, '<div class="gdtl" style="height:.*?px"><a href="(.*?)">', False)

        # 生成exh本子分页地址列表
        gPages = []
        for i in range(1, math.ceil(tempDict["pages"]/20)+1):
            gPages.append(f"https://exhentai.org/g/{item_id}/{hash_id}/?p={i}")

        #  对本子分页发出请求，获取各个分页中所有单页地址并合并到返回数据中
        subPages = thread_load_web(gPages, headers=headers)
        for k, v in subPages.items():
            temp = reglux(v.text, '<div class="gdtl" style="height:320px"><a href="(.*?)">', False)
            imagesTemp += temp
        tempDict["images"] = imagesTemp

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


@router.get("/thumb/{tid}")
async def exh_thumb(tid: str):
    # todo 处理方式还不够完美
    if len(tid) < 4:
        return Response(status_code=404)
    from handlers.getWeb import base_load_web
    headers = {
        "Cookie": random.choice(EXH_COOKIE)
    }
    url = "https://exhentai.org/t/"+tid[0]+tid[1]+"/"+tid[2]+tid[3]+"/"+tid+".jpg"
    r = base_load_web(url, headers=headers)
    return Response(content=r.content)