# coding: utf-8
import _queue
import time
from urllib.parse import urlparse
from queue import Queue

from playwright.sync_api import sync_playwright

from core.elementer import ElementHandler
from core.listener import ListerHandler
from core.repeat import RepeatHandler
from core.router import RouteHandler
from settings import browser_configs, context_configs, context_init_js, context_default_timeout


class Mundo(ListerHandler, RouteHandler, ElementHandler):
    task_queue = Queue()

    def __init__(self):
        self.playwright = sync_playwright().start()
        self.chromium = self.playwright.chromium
        self.browser = self.chromium.launch(**browser_configs)
        self.context = self.browser.new_context(**context_configs)
        self.context.add_init_script(context_init_js[0])
        self.context.set_default_timeout(context_default_timeout)  # 页面加载等待时间

    def new_page(self):
        return self.context.new_page()

    def close_page(self, page):
        page.close()

    def add_target(self, url):
        if isinstance(url, str):
            self.base_target = urlparse(url).netloc
            self.task_queue.put_nowait((url, ""))
        if isinstance(url, list):
            for _url in url:
                self.task_queue.put_nowait((url, ""))

    def run(self):
        while True:
            print("------ 新的页面 -------")
            try:
                url, request = self.task_queue.get_nowait()
                page = self.new_page()
                self.add_listener(page)
                self.homelogy_route(page)  # 拒绝非同源的请求
                page.goto(url, wait_until="networkidle")
                self.common_route(page)
                self.analyze(page)
                self.close_page(page)
            except _queue.Empty as e:
                break
            except Exception as e:
                self.close_page(page)
            except KeyboardInterrupt as e:
                for url in RepeatHandler.cache:
                    print(url)

        self.context.close()
        self.browser.close()
        self.playwright.stop()
        print("爬取结束")


if __name__ == '__main__':
    mundo = Mundo()
    url = "http://bh4ars.riskivy.xyz"
    mundo.add_target(url)
    mundo.run()
