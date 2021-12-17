# coding: utf-8
from queue import Queue
from urllib.parse import urlparse

from configs import ConfigController


class TargetHandler():
    base_target = ""
    task_queue = Queue()

    @classmethod
    def is_homelogy(cls, url):
        url_netloc = urlparse(url).netloc
        if url_netloc != ConfigController.base_url:
            return False
        return True

    @classmethod
    def add_target(cls, target):
        if isinstance(target, str):
            ConfigController.base_url = urlparse(target).netloc
            cls.task_queue.put_nowait((target, ""))
        if isinstance(target, list):
            for _url in target:
                cls.task_queue.put_nowait((_url, ""))
