#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2020/10/25 
# CreatTIME : 10:45 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
from fastapi import APIRouter
router = APIRouter()
__author__ = 'RaXianch'
app_name = 'exhentai'
EXH_COOKIE = [
    # 该cookie只能获得normal缩略图
    # "ipb_member_id=2263496; ipb_pass_hash=6d94181101e10c5e8497c22bcfdf49e5; igneous=5676ef9eb21f775ab55895d02b30e2805d616aaed60eb5f9e7e5bddeb018be5596a971e6ad5947c4c1f2cb02ef069779db694b2649da1b0bfb5a7b2a23767fa4; yay=louder; sl=dm_1;",
    # 获取large缩略图
    "ipb_member_id=5095139; ipb_pass_hash=1c9270dba822fb0f833c1e36885a8958; igneous=616f4f541; sl=dm_1;",
    "ipb_member_id=2565648; ipb_pass_hash=56c08754a7754028dadb9d7cfe9f6195; igneous=d4855c11e; sl=dm_1;",
]
