from core.analysis_page import Analysis
from core.base import MunDoBase
from core.cache import MunDoCache


class Mundo(MunDoBase, MunDoCache):
    def __init__(self, entrypoints):
        super(Mundo, self).__init__(entrypoints)
        self.analysis = Analysis(self.queue, self.base_target)

    def get_new_page(self):
        page = self.context.new_page()
        self.add_listener(page)
        return page

    def _start(self):
        url = self.queue.get()
        if not self.need_crawle(url):
            return
        print("start url: {}".format(url))
        page = self.get_new_page()
        page.goto(url, wait_until="networkidle")
        self.analysis.analysis_a(url, page)
        page.close()

    def index(self):
        for entryponit in self.entrypoints:
            self.queue.put(entryponit)

    def start(self):
        self.index()
        while self.queue.qsize() != 0:
            self._start()

        print("爬取结束")
