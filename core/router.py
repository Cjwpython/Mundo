# coding: utf-8'
from functools import partial
from urllib.parse import urlparse

import time
from utils.log import setup_logger

logger = setup_logger(__name__)
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
            if not self.is_homelogy(request_url):
                logger.debug(f"丢弃非同源的url:{request_url}")
                route.abort("aborted")
                return
            logger.debug(f"放入队列中，请求将会在新的页面打开:{request_url}:{request.method}")
            route.abort("aborted")
            self.task_queue.put_nowait((request_url, request))
            return
        route.continue_()

    def homelogy_route(self, page):
        page.route("**/*", partial(self.homelogy_handle))

    def homelogy_handle(self, route, request):
        request_url = request.url
        if RepeatHandler.request_in(request_url, request.method):
            logger.debug("去除重复的请求")
            route.abort("aborted")
            return
        if not self.is_homelogy(request_url):
            route.abort("aborted")
            # print(f"拒绝非同源的请求：{request.method} {request_url}")
            return
        route.continue_()

    def forword_route(self, page, request):
        page.route(request.url, lambda route: route.continue_(headers=request.headers, method=request.method, post_data=request.post_data))
