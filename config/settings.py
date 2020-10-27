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
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 部署服务器的地址和端口
HOST = "127.0.0.1"
PORT = 1021

# 文档开关
DOCS_URL = None
REDOC_URL = None

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
# 举例：
# CUSTO_CALLBACK_DATA = {
#     "token": "RaXianch666",
#     "example": "假如前端需要从响应的json数据中，接收某个自定义参数，就写这里",
# }
CUSTO_CALLBACK_DATA = {

}
"""
其他设置
"""
# exhentai的登陆cookie
SELF_EXH_COOKIE = [

]
