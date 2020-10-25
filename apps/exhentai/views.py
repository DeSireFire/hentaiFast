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
from fastapi import APIRouter
router = APIRouter()

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