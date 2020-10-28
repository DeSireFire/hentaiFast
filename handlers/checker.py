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


def proxy_check(ip, port, url="http://www.baidu.com/"):
    """
    代理有效性检测
    :param url:
    :param ip: str,代理ip
    :param port: str,接口
    :param url: str,需要测试的目标网址
    :return:bool,根据状态码判断是否可用
    """
    import requests
    proxies = {"http": f"http://{ip}:{port}"}
    # 空白位置为测试代理ip和代理ip使用端口

    headers = {"User-Agent": "Mozilla/5.0"}
    # 响应头
    res = requests.get(url, proxies=proxies, headers=headers)

    if 200 <= res.status_code < 300:
        return True
    return False
