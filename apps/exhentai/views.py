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
        bids = reglux(req.text, r'<a href="https://exhentai.org/g/([\s\S]*?)/([\s\S]*?)/">', False)
        names = reglux(req.text, r'class="glink">([\s\S]*?)</div>', False)
        thumbs = reglux(req.text, r'src="https://exhentai.org/t/.*?/.*?/([\s\S]*?).jpg"', False)
        # todo id&hash是否分离。星级等新字段添加
        for b, n, t in zip(bids, names, thumbs):
            tempItem = {
                "id": b[0],
                "hash": b[-1],
                "bname": n,
                "cover": "/ero/exh/thumb/%s/" % t,
                "url": "/ero/exh/id/%s/%s/" % (b[0], b[1]),
            }
            tempDict["bookList"].append(tempItem)
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
    from handlers.getWeb import base_load_web, thread_load_web
    baseDict = {
        "id": None,
        "hash": None,
        "origin": app_name,
        "title": None,
        "pages": None,
        "favorites": 0,
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

    # 请求失败返回
    if req is None:
        return callbackJson.callBacker(tempDict)

    import math
    from handlers.dbFormat import reglux
    callbackJson.statusCode = req.status_code

    # 获取本子图片总数
    tempDict["pages"] = int("".join(reglux(req.text, 'Length:</td><td class="gdt2">(.*?) pages</td></tr>', False)))
    # 获取本子首页所有单页地址
    imagesTemp = []
    # exh html 不时出现变化，双路正则表达式
    imagesTemp += reglux(req.text, '<div class="gdtl" style="height:.*?px"><a href="(.*?)">', False) or \
                  reglux(req.text, 'no-repeat"><a href="(.*?)"><img alt', False)
    # 计算exh对本子的分页数
    gPages = math.ceil(tempDict["pages"]/20)
    # 大于1页才进行多页请求
    if gPages > 1:
        # 生成exh本子分页地址列表
        gUrlPagesUrl = []
        for i in range(1, gPages+1):
            gUrlPagesUrl.append(f"https://exhentai.org/g/{item_id}/{hash_id}/?p={i}")

        #  对本子分页发出请求，获取各个分页中所有单页地址并合并到返回数据中
        subPages = thread_load_web(gUrlPagesUrl, headers=headers)
        for k, v in subPages.items():
            temp = reglux(v.text, '<div class="gdtl" style="height:.*?px"><a href="(.*?)">', False) or \
                   reglux(req.text, 'no-repeat"><a href="(.*?)"><img alt', False)
            imagesTemp += temp

    # 是否提供原生数据
    if raw:
        tempDict["raw"] = [req.text]
    else:
        del tempDict["raw"]


    # 数据整理
    tempDict["images"] = list(map(lambda x: f"/ero/exh/galleries/{x.split('/s/')[-1]}/", imagesTemp))
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


@router.get("/galleries/{book_hash}/{picture_id}/")
async def exh_manga(book_hash: str, picture_id: str,):
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


#todo 单页列表分离
#todo 单本信息接口加上分页总数
