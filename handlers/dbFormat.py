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
    """
    字符串数字提取函数
    :param tempStr: str,被提取的字符串
    :return: str,从字符串中筛出来的来数字
    """
    import re
    return re.sub(r"\D", "", tempStr)


def str_2_encrypt(tempStr, enc="utf-8"):
    import base64
    encStr = str(base64.b64encode(tempStr.encode(enc)), enc)[::-1]
    return encStr


def encrypt_2_str(encStr, enc="utf-8"):
    import base64
    decStr = str(base64.b64decode(encStr[::-1].encode(enc)), enc)
    return decStr

