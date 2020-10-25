#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2020/10/25 
# CreatTIME : 1:45 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire

__author__ = 'RaXianch'

import json
# 响应数据构建器
from apps import constructResponse

from fastapi import APIRouter
# 声明视图子路由
router = APIRouter()

# 视图函数
@router.get("/id/{item_id}")
async def nh_item(item_id: int):
    """
    依据本子id响应本子信息
    :param item_id: int,本子的唯一id
    :return: json,响应的数据咯~
    """
    from handlers.getWeb import base_load_web
    tempStr = "{}"
    callbackJson = constructResponse()
    req = base_load_web("https://nhentai.net/g/%s/" % item_id)
    if req != None:
        from handlers.dbFormat import reglux
        callbackJson.statusCode = req.status_code
        tempStr = "".join(reglux(req.text, r'window._gallery = JSON.parse\("([\s\S]*?)"\);', False)).encode(
            "utf-8").decode('unicode-escape')
    return callbackJson.callBacker(json.loads(tempStr))
