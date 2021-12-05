# coding: utf-8
import _queue
import time
from urllib.parse import urlparse
from queue import Queue

from playwright.sync_api import sync_playwright

from core.elementer import ElementHandler
from core.listener import ListerHandler
from core.router import RouteHandler


class Mundo(ListerHandler, RouteHandler, ElementHandler):
    task_queue = Queue()

    def __init__(self):
        self.playwright = sync_playwright().start()
        self.chromium = self.playwright.chromium
        self.browser = self.chromium.launch(headless=False,
                                            executable_path="/Users/wtt/pw-browsers/chromium-939194/chrome-mac/Chromium.app/Contents/MacOS/Chromium")
        self.context = self.browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            java_script_enabled=True,
            ignore_https_errors=True
        )
        self.context.add_init_script('Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});')
        self.context.set_default_timeout(300000)  # 页面加载等待时间

    def new_page(self):
        return self.context.new_page()

    def close_page(self, page):
        page.close()

    def add_target(self, url):
        if isinstance(url, str):
            self.base_target = urlparse(url).netloc
            # self.base_target = "bh4ars.riskivy.xyz"
            self.task_queue.put_nowait((url, ""))
        if isinstance(url, list):
            for _url in url:
                self.task_queue.put_nowait((url, ""))

    def run(self):
        while True:
            print("开始新的页面")
            try:
                url, request = self.task_queue.get_nowait()
                if not self.is_homelogy(url):
                    continue

                page = self.new_page()
                if request:  # 说明这个不是get 请求的
                    print("重新的方法")
                    page.route(request.url, handler=self.other_handler)
                # self.add_listener(page)
                page.goto(url, wait_until="networkidle")
                self.add_route(page, url)
                self.analyze(page)
                time.sleep(100)
                page.close()
            except _queue.Empty as e:
                break

        self.context.close()
        self.browser.close()
        self.playwright.stop()
        print("爬取结束")


if __name__ == '__main__':
    mundo = Mundo()
    url = "https://10.0.83.41/#/login"
    mundo.add_target(url)
    mundo.run()
