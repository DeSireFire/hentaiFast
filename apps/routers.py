#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2020/10/25 
# CreatTIME : 1:45 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire

__author__ = 'RaXianch'

from fastapi import APIRouter
from apps.index import views as index
from apps.nhentai import views as nhentai
from apps.exhentai import views as exhentai
routesPath = {
    "": index.router,
    "/ero/nh": nhentai.router,
    "/ero/exh": exhentai.router,
}
temp_router = APIRouter()
for u, r in routesPath.items():
    temp_router.include_router(r, prefix=u)

api_router = temp_router



