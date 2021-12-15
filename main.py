# coding: utf-8
import _queue
from urllib.parse import urlparse
from queue import Queue

from playwright.sync_api import sync_playwright

from core.elementer import ElementHandler
from core.listener import ListerHandler
from core.repeat import RepeatHandler
from core.router import RouteHandler
from settings import browser_configs, context_configs, context_init_js, context_default_timeout
import utils.log

logger = utils.log.setup_logger()


class Mundo(ListerHandler, RouteHandler, ElementHandler):
    task_queue = Queue()

    def __init__(self):
        self.playwright = sync_playwright().start()
        self.chromium = self.playwright.chromium
        self.browser = self.chromium.launch(**browser_configs)
        self.context = self.browser.new_context(**context_configs)
        for js in context_init_js:
            self.context.add_init_script(js)
        self.context.set_default_timeout(context_default_timeout)  # 页面加载等待时间

    def new_page(self):
        return self.context.new_page()

    def close_page(self, page):
        logger.debug("***** 页面关闭 *****")
        page.close()

    def add_target(self, url):
        if isinstance(url, str):
            self.base_target = urlparse(url).netloc
            self.task_queue.put_nowait((url, ""))
        if isinstance(url, list):
            for _url in url:
                self.task_queue.put_nowait((url, ""))

    def filter_repeat_page(self, url, request):
        """
        对url request 进行去重  避免 多次请求
        """
        if request:
            if RepeatHandler.request_in(request.url, request.method):
                logger.debug(f"request去重：{request.url}:{request.method}")
                return True
        else:
            if RepeatHandler.request_in(url, "GET"):
                logger.debug(f"url去重：{request.url}:GET")
                return True

    def run(self):
        while True:
            try:
                url, request = self.task_queue.get_nowait()
                if self.filter_repeat_page(url, request):
                    continue
                page = self.new_page()

                if request != "" and request.method != "GET":
                    logger.debug("------ 新的转发页面 -------")
                    self.forword_listener(page, request)
                    self.forword_route(page, request)
                    page.goto(request.url, wait_until="networkidle")
                else:
                    logger.debug("------ 新的请求页面 -------")
                    self.common_listener(page)
                    self.homelogy_route(page)  # 拒绝非同源的请求
                    page.goto(url, wait_until="networkidle")
                    self.remove_listener(page)
                    self.common_route(page)
                    self.analyze(page)
                self.close_page(page)
            except _queue.Empty as e:
                break
            except KeyboardInterrupt as e:
                for url in RepeatHandler.request_cache:
                    print(url)

        self.context.close()
        self.browser.close()
        self.playwright.stop()
        logger.info("爬取结束")
        for url in RepeatHandler.request_cache:
            print(url)


if __name__ == '__main__':
    mundo = Mundo()
    url = "http://bh4ars.riskivy.xyz/Brute%20Force/index.php"
    mundo.add_target(url)
    mundo.run()
