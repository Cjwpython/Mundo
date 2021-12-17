# coding: utf-8
from settings import page_configs


class PageController():
    wait_until = page_configs.get("wait_until", "networkidle")
    waitTime = page_configs.get("waitTime", 0)

    @classmethod
    def set_wait_until(cls, wait_until: str):
        if wait_until not in ["commit", "domcontentloaded", "load", "networkidle"]:
            raise TypeError("页面加载策略配置错误")
        cls.wait_until = wait_until

    @classmethod
    def set_waitTime(cls, waitTime: int):
        cls.waitTime = waitTime
