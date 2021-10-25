# coding: utf-8
from functools import partial
from urllib.parse import urlparse

from utils.listener import Listener


class MunDoBase():
    """
    蒙多爬虫基类
    """

    def __init__(self, entrypoints):
        # 设置入口url
        self.entrypoints = entrypoints
        self.base_target = urlparse(self.entrypoints[0]).netloc
        self.listener = Listener(self.base_target)
        # 初始化队列信息
        # 设置缓存区

    def set_browser(self, browser):
        self.browser = browser

    def set_context(self, context):
        self.context = context

    def add_listener(self, page):
        # page.on("request", log_request)
        page.on("response", partial(self.listener.log_response, page))
