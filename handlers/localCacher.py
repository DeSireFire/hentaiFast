#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2020/11/14 
# CreatTIME : 21:00 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire

__author__ = 'RaXianch'

import weakref
import time
import collections
from functools import wraps
from config.settings import LOCAL_CACHE, CACHE_TIME


class LocalCache(object):
    notFound = object()

    # list dict等不支持弱引用，但其子类支持，故这里包装了下
    class Dict(dict):
        def __del__(self):
            pass

    def __init__(self, maxlen=10):
        self.weak = weakref.WeakValueDictionary()
        self.strong = collections.deque(maxlen=maxlen)

    @staticmethod
    def nowTime():
        return int(time.time())

    def get(self, key):
        value = self.weak.get(key, self.notFound)
        if value is not self.notFound:
            expire = value[r'expire']
            if self.nowTime() > expire:
                return self.notFound
            else:
                return value
        else:
            return self.notFound

    def set(self, key, value):
        # strongRef作为强引用避免被回收
        self.weak[key] = strongRef = LocalCache.Dict(value)
        # 放入定大队列，弹出元素马上被回收
        self.strong.append(strongRef)


# 装饰器
def func_Cache(expire=CACHE_TIME or 0, CacheOn=LOCAL_CACHE or False):
    caches = LocalCache()

    def _wrappend(func):
        if CacheOn:
            @wraps(func)
            def __wrapped(*args, **kwargs):
                key = str(func) + str(args) + str(kwargs)
                result = caches.get(key)
                if result is LocalCache.notFound:
                    result = func(*args, **kwargs)
                    caches.set(key, {r'result': result, r'expire': expire + caches.nowTime()})
                    result = caches.get(key)
                return result['result']

            return __wrapped

        return func

    return _wrappend



"""
# 测试函数
import time
@funcCache(expire=300)
def test_cache(v):
    # 模拟任务处理时常3秒
    time.sleep(3)
    print('work 3s')
    return v


print(test_cache(1))
print(test_cache(2))

print(test_cache(1))
print(test_cache(2))
"""
