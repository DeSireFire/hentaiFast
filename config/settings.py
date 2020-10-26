"""
henTaiFast 配置文件
"""
import os
"""
版本号
"""
# 程序版本号，此项别动
VERSION = 1.0
"""
全局设置
"""
# debug模式
DEBUG = True

# 项目根目录
BASE_PATH = BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 部署服务器的地址和端口
HOST = "127.0.0.1"
PORT = 1021

"""
请求设置
"""
# 是否验证SSL证书
VERIFY = True
# 超时等待(单位是秒)
TIMEOUT = 6
# 重试次数
RETRY_MAX = 3
# 是否开启代理（代理总开关）
ONPROXY = True
# 代理设置
PROXY_SETTING = {
    # True全局使用代理,False则重试时才使用代理
    "reTryProxy": True,
    # 代理接口设置
    "http": "http://127.0.0.1:1080",
    "https": "http://127.0.0.1:1080",
}
"""
回调设置

即请求接口时，返回的json数据结构
"""
# 默认回调数据结构模板，BASE_CALLBACK_DATA不建议更改，也不建议覆盖。
BASE_CALLBACK_DATA = {
    "status_code": 404,
    "status_bool": False,
    "version": VERSION,
    "cost_time": None,
    "date": None,
    "ts": None,
    "message": "未知回调错误！",
    "data": {},
}

# 自定义回调数据，可添加任意自己需要的键值对，来扩充BASE_CALLBACK_DATA当中
CUSTO_CALLBACK_DATA = {
    "token": "RaXianch666",
    "扯淡": "今天的天气真好啊~",
}


