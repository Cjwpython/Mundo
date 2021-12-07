# coding: utf-8'
from functools import partial
from urllib.parse import urlparse

from core.repeat import RepeatHandler


class RouteHandler():
    def is_homelogy(self, url):
        url_netloc = urlparse(url).netloc
        if url_netloc != self.base_target:
            return False
        return True

    def common_route(self, page):
        page.route("**/*", partial(self.common_handle))

    def common_handle(self, route, request):
        request_url = request.url
        if request.is_navigation_request():
            # print("页面发生重定向")
            # print(request_url)
            route.abort("aborted")
            if not self.is_homelogy(request_url):
                return
            self.task_queue.put_nowait((request_url, request))
            return
        route.continue_()

    def homelogy_route(self, page):
        page.route("**/*", partial(self.homelogy_handle))

    def homelogy_handle(self, route, request):
        request_url = request.url
        if RepeatHandler.request_in(request_url):
            print("去除重复的请求")
            route.abort("aborted")
            return
        if not self.is_homelogy(request_url):
            route.abort("aborted")
            # print(f"拒绝非同源的请求：{request.method} {request_url}")
            return
        route.continue_()
