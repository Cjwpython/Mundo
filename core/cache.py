# coding: utf-8
from queue import  Queue


class MunDoCache():
    """
    缓存类
    """
    queue = Queue()
    cache = []

    def need_crawle(self, url):
        if url in self.cache:
            return False
        self.cache.append(url)
        return True

    def put(self, url):
        self.queue.put(url)

    def get(self):
        a = self.queue.get()
        return a
