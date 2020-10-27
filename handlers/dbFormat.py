#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2020/10/23 
# CreatTIME : 12:53 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire

__author__ = 'RaXianch'

"""
数据 格式化&清洗
"""

def reglux(rawText, re_pattern, nbsp_del=True):
    '''
    正则过滤函数
    :param rawText: 字符串，待匹配的字符串
    :param re_pattern: 字符串，正则表达式
    :param nbsp_del: 布尔值，控制是否以去除换行符的形式抓取有用信息
    :return:
    '''
    import re
    # re_pattern = re_pattern.replace('~[',"\~\[").replace(']~','\]\~')
    pattern = re.compile(re_pattern)
    if nbsp_del:
        temp = pattern.findall("".join(rawText.split()))
    else:
        temp = pattern.findall(rawText)
    if temp:
        return temp
    else:
        return []


def str_to_unicode(tempStr, enc="utf-8"):
    return tempStr.encode(enc).decode('unicode-escape')

def str_extract_num(tempStr):
    import re
    return re.sub(r"\D", "", tempStr)