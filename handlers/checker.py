#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2020/10/23 
# CreatTIME : 12:54 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire

__author__ = 'RaXianch'

"""
检查器
"""


def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip

def check_value(ipaddr):
    '''检查IP是否合法
    :param ipaddr:  string
    :return True
    '''
    addr=ipaddr.strip().split('.')
    if len(addr) != 4:
        return False
    for i in range(4):
        try:
            addr[i]=int(addr[i])
        except:
            return False
        if addr[i]<=255 and addr[i]>=0:
            pass
        else:
            return False
        i+=1
    else:
        return True

def global_IP(value):
    """
    检查是否为公网IP
    依赖check_value函数
    :return: bool
    """
    from IPy import IP
    if check_value(value):
        if IP(value).iptype() is 'PUBLIC':
            return True
    return False