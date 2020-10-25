#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2020/10/25 
# CreatTIME : 11:54 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire

__author__ = 'RaXianch'

# 从设置文件中导入有关字典，来更新回调时，响应给客户端的json数据结构
import collections
from config.settings import BASE_CALLBACK_DATA, CUSTO_CALLBACK_DATA

RES_CALLBACK = collections.OrderedDict(BASE_CALLBACK_DATA, **CUSTO_CALLBACK_DATA)
