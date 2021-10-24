import datetime

from core.analysis_page import Analysis
from core.base import MunDoBase
from core.cache import MunDoCache

from urllib.parse import urlparse


class Mundo(MunDoBase, MunDoCache):
    def __init__(self, entrypoint):
        super(Mundo, self).__init__(entrypoint)
        self.base_target = urlparse(self.entrypoint).netloc
        self.analysis = Analysis(self.queue, self.base_target)

    def get_new_page(self):
        page = self.context.new_page()
        self.add_listener(page)
        return page

    def _start(self):
        url = self.queue.get()
        if not self.need_crawle(url):
            return
        page = self.get_new_page()
        page.goto(url, wait_until="networkidle")
        self.analysis.analysis_a(url, page)
        page.close()

    def start(self):
        self.queue.put(self.entrypoint)

        while 1:
            self._start()
