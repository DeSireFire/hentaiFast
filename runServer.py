#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2020/10/25 
# CreatTIME : 11:55 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire

__author__ = 'RaXianch'

import uvicorn
if __name__ == '__main__':
    uvicorn.run(app="server.main:app", host="127.0.0.1", port=8000, reload=True)
