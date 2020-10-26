#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2020/10/25 
# CreatTIME : 1:45 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire

__author__ = 'RaXianch'

from fastapi import APIRouter
from apps import index
from apps import nhentai
from apps import exhentai
routesPath = {
    "": index.views.router,
    "/ero/nh": nhentai.views.router,
    "/ero/exh": exhentai.views.router,
}
api_router = APIRouter()
for u, r in routesPath.items():
    api_router.include_router(r, prefix=u)



