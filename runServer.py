#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2020/10/25 
# CreatTIME : 11:55 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire

__author__ = 'RaXianch'
# todo 运行文件封装，开发启动菜单
import uvicorn
from config.settings import HOST, PORT
if __name__ == '__main__':
    uvicorn.run(app="server.main:app", host=HOST, port=int(PORT), reload=True)
