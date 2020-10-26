#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2020/10/26 
# CreatTIME : 14:47 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire

__author__ = 'RaXianch'

import uvicorn
import os
import sys

try:
    from config.settings import HOST, PORT, DOCS_URL, REDOC_URL
    from server import app

except ModuleNotFoundError as e:
    # 解决终端直接运行main.py找不到项目自建模块的问题
    sys.path.append(os.path.dirname(sys.path[0]))

    from config.settings import HOST, PORT
    from server import app


def run_uvicorn(host=HOST, port=int(PORT)):
    uvicorn.run(
        app="server.main:app",
        host=host, port=port,
        docs_url=DOCS_URL,
        redoc_url=REDOC_URL,
        reload=True)


if __name__ == '__main__':
    run_uvicorn()
# todo 启动前的自检
